#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################
#
#   AutoTST - Automated Transition State Theory
#
#   Copyright (c) 2015-2018 Prof. Richard H. West (r.west@northeastern.edu)
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the 'Software'),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#
################################################################################

import os
import logging

import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdchem import Mol
import autotst
import ase
from ase import Atom, Atoms
import rmgpy
from rmgpy.molecule import Molecule as RMGMolecule
from rmgpy.species import Species as RMGSpecies

FORMAT = "%(filename)s:%(lineno)d %(funcName)s %(levelname)s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

try:
    import py3Dmol
except ImportError:
    logging.info("Error importing py3Dmol")

import numpy as np

from autotst.geometry import CisTrans, Torsion, Angle, Bond, ChiralCenter

class Species():
    """
    A class for handling molecules in AutoTST
    """
    
    def __init__(self, smiles=[], rmg_species=None):
        
        
        assert isinstance(smiles, list)

        self._conformers = None

        if ((len(smiles) != 0) and rmg_species):
            # Provide both a list of smiles and an rmg_species
            assert isinstance(rmg_species, (rmgpy.molecule.Molecule, rmgpy.species.Species))
            
            if isinstance(rmg_species, rmgpy.molecule.Molecule):
                rmg_species = RMGSpecies(molecule=[rmg_species])
                rmg_species.generate_resonance_structures()
            
            else: 
                rmg_species.generate_resonance_structures()
                
            smiles_list = []
            for rmg_mol in rmg_species.molecule:
                smiles_list.append(rmg_mol.toSMILES())
                
            for s in smiles_list:
                if s in smiles:
                    continue
                if not(s in smiles):
                    smiles.append(s)
                    
            assert len(smiles) == len(smiles_list), "The list of smiles presented does not match the possible species provided"
            
            self.smiles = smiles
            self.rmg_species = rmg_species

        elif (rmg_species and (len(smiles) == 0)):
            # RMG species provided, but not smiles
            
            assert isinstance(rmg_species, (rmgpy.molecule.Molecule, rmgpy.species.Species))
            
            if isinstance(rmg_species, rmgpy.molecule.Molecule):
                rmg_species = RMGSpecies(molecule=[rmg_species])
                rmg_species.generate_resonance_structures()
            
            else: 
                rmg_species.generate_resonance_structures()
                
            smiles = []
            for rmg_mol in rmg_species.molecule:
                smiles.append(rmg_mol.toSMILES())
              
            self.smiles = smiles
            self.rmg_species = rmg_species

                
        elif ((not rmg_species) and (len(smiles) != 0)):
            # smiles provided but not species
            
            species_list = []
            for smile in smiles:
                molecule = RMGMolecule(SMILES=smile)
                s = RMGSpecies(molecule=[molecule])
                s.generate_resonance_structures()
                species_list.append(s)
                
            for s1 in species_list:
                for s2 in species_list:
                    assert s1.isIsomorphic(s2), "SMILESs provided describe different species"
                    
            self.smiles = smiles
            self.rmg_species = species_list[0]
                    

            
        else:
            self.smiles = []
            self.rmg_species = rmg_species
            
    def __repr__(self):
        string = ""
        
        for s in self.smiles:
            string += s +" / "
            
        return '<Species "{}">'.format(string[:-3])

    @property
    def conformers(self):
        if not self._conformers:
            self._conformers = self.generate_structures()
        return self._conformers

    def generate_structure(self, smiles=None, rmg_molecule=None):
        
        return Conformer(smiles=smiles, rmg_molecule=rmg_molecule)
    
    def generate_structures(self):
        conformers = {}
        for smile in self.smiles:
            conf = self.generate_structure(smiles=smile)
            conformers[smile] = [conf]
            
        return conformers

    def generate_conformers(self, method="systematic", calculator=None):
        possible_methods = [
            "systematic",
            #"ga",
            #"es"
        ]

        assert calculator,"Please provide an ASE calculator object"
        assert method in possible_methods, "Please provide a valid conformer search method."

        from autotst.conformer.systematic import *

        for smiles, conformers in self.conformers.iteritems():
            conformer = conformers[0]
            conformer.ase_molecule.set_calculator(calculator)
            _, conformers = systematic_search(conformer)
            self.conformers[smiles] = conformers
        
        return self.conformers
        
class Conformer():
    """
    A class for generating and editing 3D conformers of molecules
    """
    def __init__(self, smiles=None, rmg_molecule=None, index=0):

        self.energy = None
        self.index = index
        
        if (smiles or rmg_molecule):
            if smiles and rmg_molecule:
                assert rmg_molecule.isIsomorphic(
                    RMGMolecule(SMILES=smiles)), "SMILES string did not match RMG Molecule object"
                self.smiles = smiles
                self.rmg_molecule = rmg_molecule

            elif rmg_molecule:
                self.rmg_molecule = rmg_molecule
                self.smiles = rmg_molecule.toSMILES()

            else:
                self.smiles = smiles
                self.rmg_molecule = RMGMolecule(SMILES=smiles)
                
                
            self.rmg_molecule.updateMultiplicity()
            self.get_mols()
            self.get_geometries()
            
                
        else:
            self.smiles = None
            self.rmg_molecule = None   
            self.rdkit_molecule = None
            self.ase_molecule = None
            self.bonds = []
            self.angles = []
            self.torsions = []
            self.cistrans = []
            self.chiral_centers = []
        
    def __repr__(self):
        return '<Conformer "{}">'.format(self.smiles)

    def copy(self):
        copy_conf = Conformer()
        copy_conf.smiles = self.smiles
        copy_conf.rmg_molecule = self.rmg_molecule.copy()
        copy_conf.rdkit_molecule = self.rdkit_molecule.__copy__()
        copy_conf.ase_molecule = self.ase_molecule.copy()
        copy_conf.get_geometries()
        return copy_conf
    
    def get_rdkit_mol(self, rmg_molecule=None):
        """
        A method for creating an rdkit geometry from an rmg mol
        """
        if not rmg_molecule:
            rmg_molecule = self.rmg_molecule

        assert rmg_molecule, "Cannot create an RDKit geometry without an RMG molecule object"
        
        RDMol = rmg_molecule.toRDKitMol(removeHs=False)
        rdkit.Chem.AllChem.EmbedMolecule(RDMol)
        self.rdkit_molecule = RDMol
        
        mol_list = AllChem.MolToMolBlock(self.rdkit_molecule).split('\n')
        for i, atom in enumerate(rmg_molecule.atoms):
            j = i + 4
            coords = mol_list[j].split()[:3]
            for k, coord in enumerate(coords):
                coords[k] = float(coord)
            atom.coords = np.array(coords)
        
        return self.rdkit_molecule
    
    def get_ase_mol(self, rmg_molecule=None):
        """
        A method for creating an ase atoms object from an rdkit mol
        """
        
        if not rmg_molecule:
            rmg_molecule = self.rmg_molecule

        if not self.rdkit_molecule:
            self.get_rdkit_mol(rmg_molecule=rmg_molecule)

        mol_list = AllChem.MolToMolBlock(self.rdkit_molecule).split('\n')
        ase_atoms = []
        for i, line in enumerate(mol_list):
            if i > 3:
                try:
                    atom0, atom1, bond, rest = line
                    atom0 = int(atom0)
                    atom0 = int(atom1)
                    bond = float(bond)
                except ValueError:
                    try:
                        x, y, z, symbol = line.split()[0:4]
                        x = float(x)
                        y = float(y)
                        z = float(z)
                        ase_atoms.append(
                            Atom(symbol=symbol, position=(x, y, z)))
                    except:
                        continue

        self.ase_molecule = Atoms(ase_atoms)
        
        return self.ase_molecule
    
    def get_mols(self, rmg_molecule=None):
        
        try:
            rmg_molecule = self.rmg_molecule
        except NameError:
            rmg_molecule = rmg_molecule
            
        rdmol = self.get_rdkit_mol()
        asemol = self.get_ase_mol()
        
        return rdmol, asemol
    
    def view(self, rdkit_molecule=None):
        """
        A method designed to create a 3D figure of the AutoTST_Molecule with py3Dmol from the rdkit_molecule
        """
        if not rdkit_molecule:
            rdkit_molecule = self.rdkit_molecule
        mb = Chem.MolToMolBlock(rdkit_molecule)
        p = py3Dmol.view(width=600, height=600)
        p.addModel(mb, "sdf")
        p.setStyle({'stick': {}})
        p.setBackgroundColor('0xeeeeee')
        p.zoomTo()
        return p.show()
    
    
    def get_bonds(self, rdkit_molecule=None, ase_molecule=None, rmg_molecule=None):
        """
        A method for identifying all of the bonds in a conformer
        """

        if not rdkit_molecule:
            rdkit_molecule = self.rdkit_molecule
        if not ase_molecule:
            ase_molecule = self.ase_molecule
        if not rmg_molecule:
            rmg_molecule = self.rmg_molecule
        rdmol_copy = rdkit_molecule

        bond_list = []
        for bond in rdmol_copy.GetBonds():
            bond_list.append((bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()))

        bonds = []
        for index, indices in enumerate(bond_list):
            i, j = indices

            length = ase_molecule.get_distance(i, j)
            center = False
            if ((rmg_molecule.atoms[i].label) and (rmg_molecule.atoms[j].label)):
                    center = True
                
            
            bond = Bond(index=index,
                        atom_indices=indices, 
                        length=length,
                        reaction_center=center)

            bonds.append(bond)
            
        self.bonds = bonds
        
        return self.bonds

    def get_angles(self, rdkit_molecule=None, ase_molecule=None):
        """
        A method for identifying all of the angles in a conforemr
        """
        if not rdkit_molecule:
            rdkit_molecule = self.rdkit_molecule
        rdmol_copy = rdkit_molecule

        if not ase_molecule:
            ase_molecule=self.ase_molecule

        angle_list = []
        for atom1 in rdmol_copy.GetAtoms():
            for atom2 in atom1.GetNeighbors():
                for atom3 in atom2.GetNeighbors():
                    if atom1.GetIdx() == atom3.GetIdx():
                        continue

                    to_add = (atom1.GetIdx(), atom2.GetIdx(), atom3.GetIdx())
                    if (to_add in angle_list) or (tuple(reversed(to_add)) in angle_list):
                        continue
                    angle_list.append(to_add)

        angles = []
        for index, indices in enumerate(angle_list):
            i, j, k = indices

            degree = ase_molecule.get_angle(i, j, k)
            ang = Angle(index=index,
                        atom_indices=indices, 
                        degree=degree,
                        mask=[])
            mask = self.get_mask(ang, rdmol_copy, ase_molecule)
            reaction_center = False

            angles.append(Angle(index=index,
                                atom_indices=indices, 
                                degree=degree, 
                                mask=mask,
                                reaction_center=reaction_center))
        self.angles = angles
        return self.angles


    def get_torsions(self, rdkit_molecule=None, ase_molecule=None):

        if not rdkit_molecule:
            rdkit_molecule = self.rdkit_molecule
        rdmol_copy = rdkit_molecule

        if not ase_molecule:
            ase_molecule = self.ase_molecule

        torsion_list = []
        for bond1 in rdmol_copy.GetBonds():
            atom1 = bond1.GetBeginAtom()
            atom2 = bond1.GetEndAtom()
            if atom1.IsInRing() or atom2.IsInRing():
                # Making sure that bond1 we're looking at are not in a ring
                continue

            bond_list1 = list(atom1.GetBonds())
            bond_list2 = list(atom2.GetBonds())

            if not len(bond_list1) > 1 and not len(bond_list2) > 1:
                # Making sure that there are more than one bond attached to
                # the atoms we're looking at
                continue

            # Getting the 0th and 3rd atom and insuring that atoms
            # attached to the 1st and 2nd atom are not terminal hydrogens
            # We also make sure that all of the atoms are properly bound together

            # If the above are satisfied, we append a tuple of the torsion our torsion_list
            got_atom0 = False
            got_atom3 = False

            for bond0 in bond_list1:
                atomX = bond0.GetOtherAtom(atom1)
                # if atomX.GetAtomicNum() == 1 and len(atomX.GetBonds()) == 1:
                # This means that we have a terminal hydrogen, skip this
                # NOTE: for H_abstraction TSs, a non teminal H should exist
                #    continue
                if atomX.GetIdx() != atom2.GetIdx():
                    got_atom0 = True
                    atom0 = atomX

            for bond2 in bond_list2:
                atomY = bond2.GetOtherAtom(atom2)
                # if atomY.GetAtomicNum() == 1 and len(atomY.GetBonds()) == 1:
                # This means that we have a terminal hydrogen, skip this
                #    continue
                if atomY.GetIdx() != atom1.GetIdx():
                    got_atom3 = True
                    atom3 = atomY

            if not (got_atom0 and got_atom3):
                # Making sure atom0 and atom3 were not found
                continue

            # Looking to make sure that all of the atoms are properly bonded to eached
            if ("SINGLE" in str(rdmol_copy.GetBondBetweenAtoms(atom1.GetIdx(), atom2.GetIdx()).GetBondType()) and
                rdmol_copy.GetBondBetweenAtoms(atom0.GetIdx(), atom1.GetIdx()) and
                rdmol_copy.GetBondBetweenAtoms(atom1.GetIdx(), atom2.GetIdx()) and
                rdmol_copy.GetBondBetweenAtoms(atom2.GetIdx(), atom3.GetIdx())):

                torsion_tup = (atom0.GetIdx(), atom1.GetIdx(),
                            atom2.GetIdx(), atom3.GetIdx())

                already_in_list = False
                for torsion_entry in torsion_list:
                    a, b, c, d = torsion_entry
                    e, f, g, h = torsion_tup

                    if (b, c) == (f, g) or (b, c) == (g, f):
                        already_in_list = True

                if not already_in_list:
                    torsion_list.append(torsion_tup)

        torsions = []
        for index, indices in enumerate(torsion_list):
            i, j, k, l = indices

            dihedral = ase_molecule.get_dihedral(i, j, k, l)
            tor = Torsion(index=index,
                          atom_indices=indices, 
                          dihedral=dihedral,
                          mask=[])
            mask = self.get_mask(tor, rdmol_copy, ase_molecule)
            reaction_center = False

            torsions.append(Torsion(index=index,
                                    atom_indices=indices,
                                    dihedral=dihedral,
                                    mask=mask,
                                    reaction_center=reaction_center))

        self.torsions = torsions
        return self.torsions

    def get_cistrans(self):
        """
        A method for identifying all possible cistrans bonds in a molecule
        """
        rdmol_copy = self.rdkit_molecule.__copy__()

        torsion_list = []
        cistrans_list = []
        for bond1 in rdmol_copy.GetBonds():
            atom1 = bond1.GetBeginAtom()
            atom2 = bond1.GetEndAtom()
            if atom1.IsInRing() or atom2.IsInRing():
                # Making sure that bond1 we're looking at are not in a ring
                continue

            bond_list1 = list(atom1.GetBonds())
            bond_list2 = list(atom2.GetBonds())

            if not len(bond_list1) > 1 and not len(bond_list2) > 1:
                # Making sure that there are more than one bond attached to
                # the atoms we're looking at
                continue

            # Getting the 0th and 3rd atom and insuring that atoms
            # attached to the 1st and 2nd atom are not terminal hydrogens
            # We also make sure that all of the atoms are properly bound together

            # If the above are satisfied, we append a tuple of the torsion our torsion_list
            got_atom0 = False
            got_atom3 = False

            for bond0 in bond_list1:
                atomX = bond0.GetOtherAtom(atom1)
                # if atomX.GetAtomicNum() == 1 and len(atomX.GetBonds()) == 1:
                # This means that we have a terminal hydrogen, skip this
                # NOTE: for H_abstraction TSs, a non teminal H should exist
                #    continue
                if atomX.GetIdx() != atom2.GetIdx():
                    got_atom0 = True
                    atom0 = atomX

            for bond2 in bond_list2:
                atomY = bond2.GetOtherAtom(atom2)
                # if atomY.GetAtomicNum() == 1 and len(atomY.GetBonds()) == 1:
                # This means that we have a terminal hydrogen, skip this
                #    continue
                if atomY.GetIdx() != atom1.GetIdx():
                    got_atom3 = True
                    atom3 = atomY

            if not (got_atom0 and got_atom3):
                # Making sure atom0 and atom3 were not found
                continue

            # Looking to make sure that all of the atoms are properly bonded to eached
            if ("DOUBLE" in str(rdmol_copy.GetBondBetweenAtoms(atom1.GetIdx(), atom2.GetIdx()).GetBondType()) and
                rdmol_copy.GetBondBetweenAtoms(atom0.GetIdx(), atom1.GetIdx()) and
                rdmol_copy.GetBondBetweenAtoms(atom1.GetIdx(), atom2.GetIdx()) and
                    rdmol_copy.GetBondBetweenAtoms(atom2.GetIdx(), atom3.GetIdx())):

                torsion_tup = (atom0.GetIdx(), atom1.GetIdx(),
                            atom2.GetIdx(), atom3.GetIdx())

                already_in_list = False
                for torsion_entry in torsion_list:
                    a, b, c, d = torsion_entry
                    e, f, g, h = torsion_tup

                    if (b, c) == (f, g) or (b, c) == (g, f):
                        already_in_list = True

                if not already_in_list:
                    cistrans_list.append(torsion_tup)


        cistrans = []

        for ct_index, indices in enumerate(cistrans_list):
            i, j, k, l = indices
            
            b0 = rdmol_copy.GetBondBetweenAtoms(i,j)
            b1 = rdmol_copy.GetBondBetweenAtoms(j,k)
            b2 = rdmol_copy.GetBondBetweenAtoms(k,l)

            b0.SetBondDir(Chem.BondDir.ENDUPRIGHT)
            b2.SetBondDir(Chem.BondDir.ENDDOWNRIGHT)

            Chem.AssignStereochemistry(rdmol_copy,force=True)

            if "STEREOZ" in str(b1.GetStereo()):
                if round(self.ase_molecule.get_dihedral(i,j,k,l), -1) == 0:
                    atom = rdmol_copy.GetAtomWithIdx(k)
                    bonds = atom.GetBonds()
                    for bond in bonds:
                        indexes = [bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()]
                        if not ((sorted([j,k]) == sorted(indexes)) or (sorted([k,l]) == sorted(indexes))):
                            break

                    for index in indexes:
                        if not (index in indices):
                            l = index
                            break

                indices = [i,j,k,l]
                stero = "Z"

            else:
                if round(self.ase_molecule.get_dihedral(i,j,k,l), -1) == 180:
                    atom = rdmol_copy.GetAtomWithIdx(k)
                    bonds = atom.GetBonds()
                    for bond in bonds:
                        indexes = [bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()]
                        if not ((sorted([j,k]) == sorted(indexes)) or (sorted([k,l]) == sorted(indexes))):
                            break

                    for index in indexes:
                        if not (index in indices):
                            l = index
                            break

                indices = [i,j,k,l]
                stero = "E"

            dihedral = self.ase_molecule.get_dihedral(i, j, k, l)
            tor = CisTrans(index=ct_index,
                           atom_indices=indices, 
                           dihedral=dihedral,
                           mask=[], 
                           stero=stero)
            mask = self.get_mask(tor)
            reaction_center = False

            cistrans.append(CisTrans(index=ct_index,
                                     atom_indices=indices, 
                                     dihedral=dihedral,
                                     mask=mask, 
                                     stero=stero
                                    )
                           )

        self.cistrans = cistrans
        return self.cistrans
    
    def get_mask(self, torsion_or_angle, rdkit_molecule=None, ase_molecule=None):

        if not rdkit_molecule:
            rdkit_molecule = self.rdkit_molecule
        rdmol_copy = rdkit_molecule

        if not ase_molecule:
            ase_molecule = self.ase_molecule



        rdkit_atoms = rdmol_copy.GetAtoms()

        if (isinstance(torsion_or_angle, autotst.geometry.Torsion) or
                isinstance(torsion_or_angle, autotst.geometry.CisTrans)):

            L1, L0, R0, R1 = torsion_or_angle.atom_indices

            # trying to get the left hand side of this torsion
            LHS_atoms_index = [L0, L1]
            RHS_atoms_index = [R0, R1]

        elif isinstance(torsion_or_angle, autotst.geometry.Angle):
            a1, a2, a3 = torsion_or_angle.atom_indices
            LHS_atoms_index = [a2, a1]
            RHS_atoms_index = [a2, a3]

        complete_RHS = False
        i = 0
        atom_index = RHS_atoms_index[0]
        while complete_RHS is False:
            try:
                RHS_atom = rdkit_atoms[atom_index]
                for neighbor in RHS_atom.GetNeighbors():
                    if (neighbor.GetIdx() in RHS_atoms_index) or (neighbor.GetIdx() in LHS_atoms_index):
                        continue
                    else:
                        RHS_atoms_index.append(neighbor.GetIdx())
                i += 1
                atom_index = RHS_atoms_index[i]

            except IndexError:
                complete_RHS = True

        mask = [index in RHS_atoms_index for index in range(
            len(ase_molecule))]

        return mask
    
    def get_chiral_centers(self):
        """
        A method to identify 
        """

        centers = rdkit.Chem.FindMolChiralCenters(self.rdkit_molecule, includeUnassigned=True)
        chiral_centers = []
        
        for index, center in enumerate(centers):
            atom_index, chirality = center
            
            chiral_centers.append(ChiralCenter(index=index, atom_index=atom_index, chirality=chirality))
            
        self.chiral_centers = chiral_centers
        return self.chiral_centers
    
    def get_geometries(self):
        """
        A helper method to obtain all geometry things
        """
        
        self.bonds = self.get_bonds()
        self.angles = self.get_angles()
        self.torsions = self.get_torsions()
        self.cistrans = self.get_cistrans()
        self.chiral_centers = self.get_chiral_centers()
        
        return (self.bonds, self.angles, self.torsions, self.cistrans, self.chiral_centers)
    
    
    def update_coords(self):
        """
        A function that creates distance matricies for the RMG, ASE, and RDKit molecules and finds which
        (if any) are different. If one is different, this will update the coordinates of the other two
        with the different one. If all three are different, nothing will happen. If all are the same,
        nothing will happen.
        """
        rdkit_dm = rdkit.Chem.rdmolops.Get3DDistanceMatrix(self.rdkit_molecule)
        ase_dm = self.ase_molecule.get_all_distances()
        l = len(self.rmg_molecule.atoms)
        rmg_dm = np.zeros((l,l))

        for i, atom_i in enumerate(self.rmg_molecule.atoms):
            for j, atom_j in enumerate(self.rmg_molecule.atoms):
                rmg_dm[i][j] = np.linalg.norm(atom_i.coords - atom_j.coords)

        d1 = round(abs(rdkit_dm - ase_dm).max(), 3)
        d2 = round(abs(rdkit_dm - rmg_dm).max(), 3)
        d3 = round(abs(ase_dm - rmg_dm).max(), 3)

        if np.all(np.array([d1,d2,d3]) > 0):
            return False, None

        if np.any(np.array([d1,d2,d3]) > 0):
            if d1 == 0:
                diff = "rmg"
                self.update_coords_from("rmg")
            elif d2 == 0:
                diff = "ase"
                self.update_coords_from("ase")
            else:
                diff = "rdkit"
                self.update_coords_from("rdkit")

            return True, diff
        else:
            return True, None

        
    def update_coords_from(self, mol_type="ase"):
        """
        A method to update the coordinates of the RMG, RDKit, and ASE objects with a chosen object.
        """
        
        possible_mol_types = ["ase", "rmg", "rdkit"]
        
        assert (mol_type.lower() in possible_mol_types), "Please specifiy a valid mol type. Valid types are {}".format(possible_mol_types)
        
        if mol_type.lower() == "rmg":
            conf = self.rdkit_molecule.GetConformers()[0]
            ase_atoms = []
            for i, atom in enumerate(self.rmg_molecule.atoms):
                x, y, z = atom.coords
                symbol = atom.symbol

                conf.SetAtomPosition(i, [x, y, z])

                ase_atoms.append(Atom(symbol=symbol, position=(x, y, z)))

            self.ase_molecule = Atoms(ase_atoms)
            
        elif mol_type.lower() == "ase":
            conf = self.rdkit_molecule.GetConformers()[0]
            for i, position in enumerate(self.ase_molecule.get_positions()):
                self.rmg_molecule.atoms[i].coords = position
                conf.SetAtomPosition(i, position)
                
        elif mol_type.lower() == "rdkit":
            
            mol_list = AllChem.MolToMolBlock(self.rdkit_molecule).split('\n')
            for i, atom in enumerate(self.rmg_molecule.atoms):
                j = i + 4
                coords = mol_list[j].split()[:3]
                for k, coord in enumerate(coords):
                    coords[k] = float(coord)
                atom.coords = np.array(coords)
                
            self.get_ase_mol()
            
            
    def set_bond_length(self, bond_index, length):
        return None
    
    def set_angle(self, angle_index, angle):
        """
        A method that will set the angle of an Angle object accordingly
        """
        
        assert isinstance(angle, (int, float)), "Plese provide a float or an int for the angle"
        
        matched = False
        for angle in self.angles:
            if angle.index == angle_index:
                matched = True
                break
                
        if not matched:
            print "Angle index provided is out of range. Nothing was changed."
            return self
            
        i,j,k = angle.atom_indices
        self.ase_molecule.set_angle(
            a1=i,
            a2=j,
            a3=k,
            a4=l,
            angle=angle,
            mask=angle.mask
        )
        
        angle.degree = angle
        
        self.update_coords_from(mol_type="ase")
        
        return self
    
    def set_torsion(self, torsion_index, dihedral):
        """
        A method that will set the diehdral angle of a Torsion object accordingly.
        """
        
        assert isinstance(dihedral, (int, float)), "Plese provide a float or an int for the diehdral angle"
        
        matched = False
        for torsion in self.torsions:
            if torsion.index == torsion_index:
                matched = True
                break
                
        if not matched:
            print "Torsion index provided is out of range. Nothing was changed."
            return self
            
        i,j,k,l = torsion.atom_indices
        self.ase_molecule.set_dihedral(
            a1=i,
            a2=j,
            a3=k,
            a4=l,
            angle=dihedral,
            mask=torsion.mask
        )
        torsion.dihedral = dihedral
        
        self.update_coords_from(mol_type="ase")
        
        return self
    
    def set_cistrans(self, cistrans_index, stero="E"):
        """
        A module that will set a corresponding cistrans bond to the proper E/Z config
        """

        assert stero.upper() in ["E", "Z"], "Please specify a valid stero direction."
        
        matched = False
        for cistrans in self.cistrans:
            if cistrans.index == cistrans_index:
                matched = True
                break
        
        if not matched:
            print "CisTrans index provided is out of range. Nothing was changed."
            return self
            
        if cistrans.stero == stero.upper():
            self.update_coords_from("ase")
            return self
        
        else:
            i,j,k,l = cistrans.atom_indices
            self.ase_molecule.rotate_dihedral(
                a1=i,
                a2=j,
                a3=k,
                a4=l,
                angle=float(180),
                mask=cistrans.mask
            )
            cistrans.stero = stero.upper()
                
            self.update_coords_from(mol_type="ase")
            return self
        
        
    def set_chirality(self, chiral_center_index, stero="R"):
        """
        A module that can set the orientation of a chiral center.
        """
        assert stero.upper() in ["R", "S"], "Specify a valid stero orientation"
                
        centers_dict = {
            'R' : Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CW,
            'S' : Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CCW
        }
        
        assert isinstance(chiral_center_index, int), "Please provide an integer for the index"
        
        rdmol = self.rdkit_molecule.__copy__()
        
        chiral_centers = self.chiral_centers
        
        match = False
        for chiral_center in self.chiral_centers:
            if chiral_center.index == chiral_center_index:
                match = True
                break
                
        if not matched:
            print "ChiralCenter index provided is out of range. Nothing was changed"
            return self

        

        rdmol.GetAtomWithIdx(chiral_center_index).SetChiralTag(centers_dict[chirality.upper()])
        
        rdkit.Chem.rdDistGeom.EmbedMolecule(rdmol)
        
        old_torsions = self.torsions[:] + self.cistrans[:]

        self.rdkit_molecule = rdmol
        self.update_coords_from(mol_type="rdkit")
        
        # Now resetting dihedral angles in case if they changed.
        
        for torsion in old_torsions:
            dihedral = torsion.dihedral
            i,j,k,l = torsion.indices
            
            self.ase_molecule.set_dihedral(
                a1 = i,
                a2 = j,
                a3 = k,
                a4 = l,
                mask = torsion.mask,
                angle = torsion.dihedral,
            )
            
        self.update_coords_from(mol_type="ase")
        
        return self
            
    