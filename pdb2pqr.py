#	Code to generate APBS compatible pqr file using PDB and force field files
#       Krishnakanth B,
#       Theoretical Biophysics Laboratory, Molecular Biophysics Unit,
#       Indian Institute of Science, Bangalore - 560012
#
#       Last Modified: May 20, 2022

#  Load the required packages
import numpy as np
import sys

ff_data = np.loadtxt("my_charmm.dat", dtype = str)
pdb_filename = sys.argv[1]
pqr_file = open(sys.argv[2],"w")

#Function to read a .pdb file, obeys 1996 nomenclature of .pdb file
def pdb_reader(pdb_filename):
	print("Reading pdb file: "+pdb_filename)
	x, y, z,res_id,atom_id ,atom_type,res_type,res_no,chain_id = [],[],[],[],[],[],[],[],[]
	f=open(pdb_filename,"r").readlines()
	for i in range(len(f)):
		if(f[i][0:4]=="ATOM"):
			x.append(float(f[i][30:38]))
			y.append(float(f[i][38:46]))
			z.append(float(f[i][46:54]))
			atom_id.append(str.strip(f[i][6:11]))
			atom_type.append(str.strip(f[i][12:16]))
			res_type.append(str.strip(f[i][17:21]))
			res_no.append(str.strip(f[i][22:26]))
			chain_id.append(f[i][21])
	return (x,y,z, atom_id, atom_type, res_type, res_no, chain_id)

x,y,z, atom_id, atom_type, res_type, res_no, chain_id =pdb_reader(pdb_filename)

def which(x, vec):
	req = []
	for i in range(len(vec)):
		if(x==vec[i]):
			req.append(i)
	return(req)


charge = []
radius = []

for i in range(len(res_type)):
	temp = list(set(which(res_type[i],ff_data[:,0])) & set(which(atom_type[i],ff_data[:,1])) )
	if(len(temp)==1):
		charge.append(float(ff_data[temp,2]))
		radius.append(float(ff_data[temp,3]))
	
	else:
		print("Something wrong.. check your files  "+res_type[i]+"  "+atom_type[i])

atom_counter = 0
for i in range(len(x)):
	atom_counter = atom_counter + 1
	atom_info = str.rjust(str(atom_id[i]),5)+" "+str.rjust(atom_type[i],3)
	res_info = str.rjust(res_type[i],4) + " "+" "+str.rjust(res_no[i],4)
	coord_info = str.rjust('%.3f'%(x[i]),8)+str.rjust('%.3f'%(y[i]),8)+str.rjust('%.3f'%(z[i]),8)+str.rjust('%.4f'%(charge[i]),8)+str.rjust('%.4f'%(radius[i]),8)
	print("ATOM  "+atom_info+"  "+res_info+"    "+coord_info,file = pqr_file)	


charges = np.loadtxt("my_charmm.dat", usecols = (2)) 




