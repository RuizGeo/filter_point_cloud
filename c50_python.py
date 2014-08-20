#create classes factor
res = robjects.FactorVector(d[0,:])
c50.C5_0()
#Create DataFrame
r=np.array([20,23,34,45,56])
r_n=robjects.FactorVector(r)
dataf = robjects.DataFrame({})
d={'r':r_n,'g':g_n,'b':b_n}
dataf = robject.DataFrame(d)
ad=c50.C5_0(dataf,classes,triasl=10,control=(c50.C5_0Control(minCases = 2, CF = 0.2)))
#Ler ad
