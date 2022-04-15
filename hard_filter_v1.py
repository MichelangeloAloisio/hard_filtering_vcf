#!/usr/bin/env pyhton
import os
import pandas as pd

Low_heterozygous_cutoff=40
High_heterozygous_cutoff=60

if Low_heterozygous_cutoff >= High_heterozygous_cutoff:
	exit('Low filter is major than High filter, change It and start again... ')

for filename in os.listdir(os.getcwd()):
	if 'multianno.txt' in filename:
		print('File Name: ', filename)
		df=pd.read_csv(filename, sep='\t', header=0,encoding = "ISO-8859-1")
		mean_coverage=df['Otherinfo3'].mean()
		percentage_10=int(mean_coverage*30/100)## percentuale del coverage da eliminare
		df_boolean=df['Otherinfo3']>percentage_10
		df_filtered_by_coverage=df[df_boolean]
		print('The row deleted are ', str(df.shape[0]-df_filtered_by_coverage.shape[0]))
		boolean_list_to_add=[]
		for x in df_filtered_by_coverage['Otherinfo13'].to_list():
			if str(x.strip().split(':')[0]) == '1|1':
				boolean_list_to_add.append(True)
			elif str(x.strip().split(':')[0]) == '1/1':
				boolean_list_to_add.append(True)
			else:
				element_1=x.strip().split(':')[1].split(',')[0]
				element_2=x.strip().split(':')[1].split(',')[1]
				if int(element_1)==0 and int(element_2)==0:
					boolean_list_to_add.append(False)
				else:
					percentage=round(int(element_1)*100/(int(element_1)+int(element_2)),2)
					if Low_heterozygous_cutoff  <= percentage <= High_heterozygous_cutoff:
						boolean_list_to_add.append(True)
					else:
						boolean_list_to_add.append(False)

		print('CTRL transformation Eterozygous unbalanced', len(df_filtered_by_coverage), len(boolean_list_to_add))
		if len(df_filtered_by_coverage)/len(boolean_list_to_add)!=1:
			exit('error in CTRL transformation ')
		#print(df_filtered_by_coverage)
		df_filtered_by_coverage.insert(df_filtered_by_coverage.shape[1], 'Eterozygous_Boolean', boolean_list_to_add)
		Filtered_df=df_filtered_by_coverage[df_filtered_by_coverage['Eterozygous_Boolean']]
		print(Filtered_df)
		Filtered_df.to_csv('./RESULTS/HARD_FILTERED_multianno_HET_CUT_OFF'+str(Low_heterozygous_cutoff)+'_'+str(High_heterozygous_cutoff)+'_'+filename+'.csv', sep=';', index=False)


			




		







