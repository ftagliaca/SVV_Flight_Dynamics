import numpy as np
import control.matlab as ml
import control as c
import matplotlib.pyplot as plt
import cmath
import math

if True:
    #Unit conversions
    def kts2mps(vInKts):
        return 0.514444 * vInKts

    def deg2rad(angleInDeg):
        return np.radians(angleInDeg)

    def lbs2Kg(weightInLbs):
        return 0.453592 * weightInLbs

    def celsius2K(tempInCelsius):
        return tempInCelsius + 273.15

    def getInitialCondition(path,fileName,index):
        file = open(path+fileName)
        lines = file.readlines()
        file.close()
        data = np.genfromtxt(lines)
        return data[index]

    def getData(path,fileName,startIndex,endIndex):
        file = open(path+fileName)
        lines = file.readlines()
        file.close()
        data = np.genfromtxt(lines)
        return data[startIndex:endIndex]

    def minutes2Seconds(minutes):
        return 60 * minutes

    def calculateSideslip():
            file = open(path+ "Body Yaw Rate[deg_p_s].csv")
            lines = file.readlines()
            file.close()

            yawRates = np.genfromtxt(lines)[indexStart:indexEnd]
            sideslip = [-beta_0]
            print(sideslip)
            for i in range(1,len(yawRates)):
                sideslip.append(-yawRates[i]*dt + sideslip[-1])

            return np.array(sideslip)

    #Standard atmosphere
    g = 9.80665
    T0 = 288.15
    a = -0.0065
    rho_0 = 1.225
    R = 287
    m0 = 5832.05389

tStart =  minutes2Seconds(58)
tEnd =    minutes2Seconds(60)
dt = 0.1
indexStart = int((1/dt)*tStart)
indexEnd  = int((1/dt)*tEnd)

path = r"C:\Users\Ivo Janssen\Documents\GitHub\SVV_Fligh_Dynamics\flight_data\matlab_files\\"
print("Program initiated with Path: ", path)



#Initial conditions and parameters
if True:    #I'm just adding this if-statement so I can collapse the whole block with constant parameters - Max
    span = 15.911
    chord = 2.0569
    S = 30.00
    Aspect_ratio = span**2/S


    fuelUsed = 0 #lbs2Kg(getInitialCondition(path,"calculated fuel used by fuel mass flow[lbs].csv",indexStart))
    ####INPUTS, Change before use
    V = kts2mps(getInitialCondition(path,"True Airspeed[knots].csv",indexStart))
    u_0= V
    mass = m0-fuelUsed
    Weight = mass*g
    T = celsius2K(getInitialCondition(path,"Static Air Temperature[deg C].csv",indexStart))
    density  = rho_0*(T/T0)**(-(g/(a*R))-1)

    D_b = span/V
    D_c = chord / V

    UseRealData = True
    if UseRealData:
        alpha_0 = deg2rad(getInitialCondition(path, "Angle of attack[deg].csv", indexStart))
        theta_0 = deg2rad(getInitialCondition(path, "Pitch Angle[deg].csv", indexStart))
        q_0 = deg2rad(getInitialCondition(path, "Body Pitch Rate[deg_p_s].csv", indexStart)) * chord / V
        beta_0 = 0
        phi_0 = deg2rad(getInitialCondition(path, "Roll Angle[deg].csv", indexStart))
        p_0 = deg2rad(getInitialCondition(path, "Body Roll Rate[deg_p_s].csv", indexStart)) * (span / (2 * V))
        r_0 = deg2rad(getInitialCondition(path, "Body Yaw Rate[deg_p_s].csv", indexStart)) * (span / (2 * V))
    else:
        alpha_0 = 0
        theta_0 = 0
        q_0 = 0
        beta_0 = 0
        phi_0 = 0
        p_0 = 0
        r_0 = 0

    #Flight test values
    oswald_factor = 0.8797482096696121
    CD_0 = 0.0297851584886189
    CL_alpha = 4.345

    mu_b = mass / (density*S*span)
    #print(mu_b)
    mu_c = mass / (density * S * chord)
    Kx = np.sqrt(0.019)
    Ky = np.sqrt(1.25*1.114)
    Kz = np.sqrt(0.042)
    Kxz = 0.002

    CL = 2*Weight/(density*V**2*S)
    #print(CL)
    CD = CD_0 + ((CL_alpha*alpha_0)**2/(np.pi*Aspect_ratio*oswald_factor))

    ### Stability Derivatives ###
    #Cx_0 = Weight * np.sin(theta_0)/(0.5*density*V**2*S)
    #Cx_q = -0.28170
    #Cx_u = -0.095

    #Cx_alpha = 0.47966
    #Cx_alpha_dot = 0.08330
    #Cx_delta_e = -0.03728

    #Cy_beta = -0.75000
    #Cy_beta_dot = 0
    #Cy_p = -0.0304
    #Cy_r = 0.8495
    #Cy_delta_a = -0.0400
    #Cy_delta_r = 0.23

    #Cz_alpha = -5.74340
    #Cz_alpha_dot = -0.0035
    #Cz_0 = -Weight*np.cos(theta_0)/(0.5*density*V**2*S)
    #Cz_u = -0.37616
    #Cz_q = -5.66290
    #Cz_delta_e = -0.69612

    #Cl_beta = -0.10260
    #Cl_p = -0.71085
    #Cl_r = 0.23760
    #Cl_delta_a = -0.23088
    #Cl_delta_r = 0.03440

    #Cn_beta = 0.1348
    #Cn_beta_dot = 0
    #Cn_p = -0.0602
    #Cn_r = -0.2061
    #Cn_delta_a = -0.0120
    #Cn_delta_r = -0.0939

    ##Flight test data used
    #Cm_q = -8.79415
    #Cm_u = 0.06990
    #Cm_alpha = -0.550
    #Cm_alpha_dot = 0.1780
    #Cm_delta_e = -1.216



    # Stability Derivatives ### WITHOUT FILTERING BUT STILL WORKING
    Cx_0 = Weight * np.sin(theta_0)/(0.5*density*V**2*S)
    Cx_q = -0.28170
    Cx_u = -0.101

    Cx_alpha = 0.47966
    Cx_alpha_dot = 0.08330
    Cx_delta_e = -0.03728

    Cy_beta = -0.75000
    Cy_beta_dot = 0
    Cy_p = -0.0304
    Cy_r = 0.8495
    Cy_delta_a = -0.0400
    Cy_delta_r = 0.23

    Cz_alpha = -3.8
    Cz_alpha_dot = -0.0035
    Cz_0 = -Weight*np.cos(theta_0)/(0.5*density*V**2*S)
    print(Cz_0)
    Cz_u = -0.525
    Cz_q = -5.66290
    Cz_delta_e = -0.69612

    Cl_beta = -0.10260
    Cl_p = -0.71085
    Cl_r =  -0.2#0.237#-0.2#0.237#-0.1
    Cl_delta_a = -0.23088
    Cl_delta_r = 0.03440

    Cn_beta = 0.106
    Cn_beta_dot = 0
    Cn_p = -0.0602
    Cn_r = -0.1636
    Cn_delta_a = -0.0120
    Cn_delta_r = 0.0939

    #Flight test data used
    Cm_q = -4
    Cm_u = 0.06990
    Cm_alpha = -0.550
    Cm_alpha_dot = 0.1780
    Cm_delta_e = -1.216


	#STABILITY DERIVATIVES WITH FILTERING WITHOUD EXPLODING
    #Cx_0 = Weight * np.sin(theta_0)/(0.5*density*V**2*S)
    #Cx_q = -0.28170
    #Cx_u = -1.085

    #Cx_alpha = 0.47966
    #Cx_alpha_dot = 0.08330
    #Cx_delta_e = -0.03728

    #Cy_beta = -0.75000
    #Cy_beta_dot = 0
    #Cy_p = -0.0304
    #Cy_r = 0.8495
    #Cy_delta_a = -0.0400
    #Cy_delta_r = 0.23

    #Cz_alpha = -5.74340
    #Cz_alpha_dot = -0.0035
    #Cz_0 = -Weight*np.cos(theta_0)/(0.5*density*V**2*S)
    #Cz_u = -0.525
    #Cz_q = -5.66290
    #Cz_delta_e = -0.69612

    #Cl_beta = -0.10260
    #Cl_p = -0.71085
    #Cl_r = 0.23760
    #Cl_delta_a = -0.23088
    #Cl_delta_r = 0.03440

    #Cn_beta = 0.099
    #Cn_beta_dot = 0
    #Cn_p = -0.0602
    #Cn_r = -0.123
    #Cn_delta_a = -0.0120
    #Cn_delta_r = 0.0939

    ##Flight test data used
    #Cm_q = -8.79415
    #Cm_u = 0.06990
    #Cm_alpha = -0.550
    #Cm_alpha_dot = 0.1780
    #Cm_delta_e = -1.216

#Old EoM Matrices
if False:
### Equation of Motion Matrices - V1 (Outdated) ###
#C1sym = np.matrix([[(-2*mu_c*chord)/(V**2),					0,								0,											0],
#				   [0,										(Cz_alpha_dot-2*mu_c)*chord/V,		0,											0],
#				   [0,										0,								-chord/V,									0],
#				   [0,										Cm_alpha_dot*chord/V,				0,										-2*mu_c*Ky**2*chord**2/(V**2)]])

#C2sym = np.matrix([[Cx_u/V,								Cx_alpha,						Cz_0,										Cx_q*chord/V],
#				   [Cz_u/V,									Cz_alpha,						-Cx_0,										(Cz_q+2*mu_c)*chord/V],
#				   [0,										0,								0,											chord/V],
#				   [Cm_u/V,									Cm_alpha,						0,											Cm_q*chord/V]])

#C3sym = np.matrix([[Cx_delta_e],
#				   [Cz_delta_e],
#				   [0],
#				   [Cm_delta_e]])


#C1asym = np.matrix([[(Cy_beta_dot-2*mu_b)*span/V,			0,								0,											0],
#					[0,										-span/(2*V),					0,											0],
#					[0,										0,								(-4*mu_b*Kx**2*span**2)/(2*V**2),			(4*mu_b*Kxz*span**2)/(2*V**2)],
#					[(Cn_beta_dot*span)/(2*V),				0,								(4*mu_b*Kxz*span**2)/(2*V**2),				(-4*mu_b*Kz**2*span**2)/(2*V**2)]])

#C2asym = np.matrix([[Cy_beta,								CL,								Cy_p*span/(2*V),							(Cy_r - 4*mu_b)*span/(2*V)],
#					[0,										0,								span/(2*V),									0],
#					[Cl_beta,								0,								Cl_p*span/(2*V),							Cl_r*span/(2*V)],
#					[Cn_beta,								0,								Cn_p*span/(2*V),							Cn_r*span/(2*V)]])

#C3asym = np.matrix([[Cy_delta_a,							Cy_delta_r],
#					[0,										0],
#					[Cl_delta_a,							Cl_delta_r],
#					[Cn_delta_a,							Cn_delta_r]])
    pass

#EoM Matrices
if True:    #EoM Matrices
    ### Equation of Motion Matrices - V2 ###
    C1sym = D_c*np.matrix([[-2*mu_c			,						0,								0,											0],
                            [0,										(Cz_alpha_dot-2*mu_c),			0,											0],
                            [0,										0,								-1		,									0],
                            [0,										Cm_alpha_dot		,			0,											-2*mu_c*Ky**2]])

    C2sym = np.matrix([[Cx_u,									Cx_alpha,						Cz_0,										Cx_q],
                       [Cz_u,									Cz_alpha,						-Cx_0,										Cz_q+2*mu_c],
                       [0,										0,								0,											1],
                       [Cm_u,									Cm_alpha,						0,											Cm_q]])

    C3sym = np.matrix([[Cx_delta_e],
                       [Cz_delta_e],
                       [0],
                       [Cm_delta_e]])

    C1asym = D_b* np.matrix([[(Cy_beta_dot-2*mu_b),					0,								0,											0],
                            [0,										-0.5,							0,											0],
                            [0,										0,								-4*mu_b*Kx**2,								4*mu_b*Kxz],
                            [Cn_beta_dot,							0,								4*mu_b*Kxz,									-4*mu_b*Kz**2]])

    C2asym = np.matrix([[Cy_beta,								CL,								Cy_p,										Cy_r - 4*mu_b],
                        [0,										0,								1,											0],
                        [Cl_beta,								0,								Cl_p,										Cl_r],
                        [Cn_beta,								0,								Cn_p,										Cn_r]])

    C3asym = np.matrix([[-Cy_delta_a,							Cy_delta_r],
                        [0,										0],
                        [-Cl_delta_a,							Cl_delta_r],
                        [-Cn_delta_a,							Cn_delta_r]])

    Asym = -np.linalg.inv(C1sym)*C2sym
    Bsym = -np.linalg.inv(C1sym)*C3sym


    Aasym = -np.linalg.inv(C1asym)*C2asym
    # Aasym[0] = [0,0,0,2/D_b]
    Basym = -np.linalg.inv(C1asym)*C3asym   #E  #

def PrintAB(ShouldPrint):
    '''
    Can be used to print the A and B matrices of both the symmetric and asymmetric motions
    :param ShouldPrint: True/False - determines if the matrices will be printed
    :return: Nothing (it does print stuff though :D )
    '''
    if ShouldPrint is True:
        print("symmetric: ")
        print("A: ", Asym)
        print("B: ", Bsym)
        print(V / chord)

        print("Asymmetric: ")
        print("A: ", Aasym)
        print("B: ", Basym)

def PrintStabilityDerivatives(ShouldPrint):
    '''
    Can be used to print a selection of stability derivatives
    :param ShouldPrint: if True, the derivatives will be printed
    :return: None (it does print stuff though :D )
    '''
    if ShouldPrint is True:
        print("debug: ")
        print("cy_beta_dot = ", Cy_beta_dot)
        print("mu_b = ", mu_b)
        print("Cn_bet_dot = ", Cn_beta_dot)
        print("Kx = ", Kx)
        print("Kz = ", Kz)
        print("Kxz = ", Kxz)
        print("Db = ", D_b)

        print("C1-1 = ", np.linalg.inv(C1asym))

        print("C2 = ", C2asym)


Csym = np.matrix(np.identity(4))
Casym = np.matrix(np.identity(4))


Dsym = np.matrix([[0],
                  [0],
                  [0],
                  [0]])
Dasym = np.matrix([[0,0],
                   [0,0],
                   [0,0],
                   [0,0]])

systemSym = ml.ss(Asym, Bsym, Csym, Dsym)
systemAsym = ml.ss(Aasym, Basym, Casym, Dasym)

Tin = np.arange(0,tEnd-tStart,0.1)
Uin = np.zeros_like(Tin)
Uin[0:30] = np.radians(5)


Uin = deg2rad(getData(path,"Deflection_of_elevator[deg].csv",indexStart,indexEnd))
Uin = Uin - Uin[0]
#print(Uin)

#plt.figure()
#plt.plot(Tin,np.degrees(Uin))

print(len(Tin),len(Uin))


TSym, ySym, xOut = c.forced_response(systemSym, T = Tin, U = Uin, X0 = [0, 0, 0, 0])
# ySym, TSym = ml.step(systemSym,X0=[0,alpha_0,theta_0,0],T = Tin)

ySym[0] = (ySym[0]*u_0 + u_0)/0.5144
ySym[1] = ((ySym[1] + alpha_0)*180/np.pi)
ySym[2] = (ySym[2]+theta_0) * 180/np.pi
ySym[3] = ((ySym[3]*(u_0 / chord))+q_0)*180/np.pi

#yAsym, TAsym = ml.impulse(systemAsym,X0=[0,0,0,0],T=Tin,input = 0)

Uaileron = deg2rad(getData(path,"Deflection of aileron (right wing)[deg].csv",indexStart,indexEnd))
Urudder = deg2rad(getData(path,"Deflection of rudder[deg].csv",indexStart,indexEnd))
Uaileron = Uaileron - np.average(Uaileron)
Uaileron[(Uaileron<0.01) & (Uaileron>-0.01)] = 0
Urudder = Urudder - np.average(Urudder)
Urudder[(Urudder<0.01) & (Urudder>-0.01)] = 0
UinAsym = np.zeros((len(Urudder),2))
UinAsym[:,0] = Uaileron
UinAsym[:,1] = Urudder

#This is only for the Damped Dutch Roll Case.
def DutchRollYawDamped():
    UDDR = np.array([[np.radians(-10)]*10, [0,0,0,0,0,0,0,0,0,0]])
    TDDR = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    for index in range(indexStart, indexEnd):
        TDDR, yDDR, xDDR = c.forced_response(systemAsym, TDDR, UDDR, X0 = [0,0,0,0])
        np.hstack([UDDR, np.array([[-0.2*yDDR[0,-1]], [0]])])
        np.hstack([TDDR, np.array([float(TDDR[-1]) + 0.1])])
        if index +1 >= indexEnd:
            return TDDR, yDDR, xDDR



TAsym, yAsym, xOutAsym = c.forced_response(systemAsym,T = Tin,U=np.transpose(UinAsym),X0=[0,0,0,0])
#TAsym, yAsym, xOutAsym = DutchRollYawDamped()
print('TAsym', TAsym)
print('yASym', yAsym)
print('xOutAsym', xOutAsym)
yAsym[0] = np.degrees((yAsym[0]+beta_0))
yAsym[1] = np.degrees((yAsym[1]+phi_0))
yAsym[2] = np.degrees((yAsym[2] * ((2*u_0)/span))+(p_0*2*u_0)/span)
yAsym[3] = np.degrees((yAsym[3] * ((2*u_0)/span))+(r_0*2*u_0)/span)



def PrintEigvals(ShouldPrint):
    '''
    Can be used to print the eigenvalues of the symmetric and asymmetric systems
    :param ShouldPrint: if True, the eigenvalues will be printed
    :return: None (it does print stuff though :D )
    '''
    if ShouldPrint is True:
        print("Eigenvalues symmetric case: \n", np.linalg.eigvals(systemSym.A))
        print("Eigenvalues asymmetric case: \n", np.linalg.eigvals(systemAsym.A))

### “In the beginning the Universe was created. This has made many people very angry and has been widely regarded as a bad move.” - Douglas Adams, The Hitchhiker's Guide to the Galaxy###

def PlotSym(ShouldPlot, t_min, t_max):
    '''
    Can be used to plot the response of the symmetric system to a disturbance
    :param ShouldPlot: if True, will plot the response
    :return: None (it does plot stuff though :D )
    '''

    t_measured = []
    with open(path + "UTC Seconds[sec].csv") as t_data:
        i = 3            #time measurements in 'UTC Seconds [sec]' start at xxx.5 secs
        t_0 = 39568.5    #the initial time as seen in 'UTC Seconds [sec]'
        for t_point in t_data.readlines():
            t_measured.append(float(t_point.strip()) - t_0 - t_min + (i%10)/10)
            i += 1
    idx_min = int(t_min*10)
    idx_max = int(t_max*10)
    t_measured = t_measured[idx_min:idx_max]

    def generate_data(filename):
        y = []
        with open(path + filename + ".csv") as file:
            for data_point in file.readlines():
                y.append(float(data_point.strip()))
        return y[idx_min:idx_max]

    if ShouldPlot is True:
        plt.figure()
        plt.subplot(2, 2, 1)
        plt.plot(TSym, ySym[0], label = 'approximate')
        plt.plot(t_measured, generate_data("True Airspeed[knots]"), label = 'measured')
        plt.legend()
        plt.grid()
        plt.ylabel("True Airspeed [m/s]")
        plt.xlabel("Time since Start Manoeuvre [s]")
        plt.subplot(2, 2, 2)
        plt.plot(TSym, ySym[1], label = 'approximate')
        plt.plot(t_measured, generate_data("Angle of attack[deg]"), label = 'measured')
        plt.legend()
        plt.grid()
        plt.ylabel("Angle of Attack [deg]")
        plt.xlabel("Time since Start Manoeuvre [s]")
        plt.subplot(2, 2, 3)
        plt.plot(TSym, ySym[2], label = 'approximate')
        plt.plot(t_measured, generate_data("Pitch Angle[deg]"), label = 'measured')
        plt.legend()
        plt.grid()
        plt.ylabel("Pitch Angle [deg]")
        plt.xlabel("Time since Start Manoeuvre [s]")
        plt.subplot(2, 2, 4)
        plt.plot(TSym, ySym[3], label = 'approximate')
        plt.plot(t_measured, generate_data("Body Pitch Rate[deg_p_s]"), label = 'measured')
        #plt.plot(t_measured,np.degrees(Uin),label = "Elevator")
        plt.legend()
        plt.grid()
        plt.ylabel("Pitch Rate [deg/s]")
        plt.xlabel("Time since Start Manoeuvre [s]")

def PlotAsym(ShouldPlot, t_min, t_max):
    '''
    Can be used to plot the response of the symmetric system to a disturbance
    :param ShouldPlot: if True, will plot the response
    :return: None (it does plot stuff though :D )
    '''

    t_measured = []
    with open(path + "UTC Seconds[sec].csv") as t_data:
        i = 3            #time measurements in 'UTC Seconds [sec]' start at xxx.5 secs
        t_0 = 39568.5    #the initial time as seen in 'UTC Seconds [sec]'
        for t_point in t_data.readlines():
            t_measured.append(float(t_point.strip()) - t_0 - t_min + (i%10)/10)
            i += 1
    idx_min = int(t_min*10)
    idx_max = int(t_max*10)
    t_measured = t_measured[idx_min:idx_max]

    def generate_data(filename):
        y = []
        with open(path + filename + ".csv") as file:
            for data_point in file.readlines():
                y.append(float(data_point.strip()))

        
        return y[idx_min:idx_max]

    if ShouldPlot is True:
        plt.figure()
        plt.subplot(2, 2, 1)
        plt.plot(TAsym, yAsym[0], label = 'approximate')
        plt.plot(t_measured, calculateSideslip(), label = 'measured') #PLOTTING A DIFFERENT VALUE AS I DO NOT HAVE A FILE FOR SIDESLIP ANGLE
        plt.legend()
        plt.grid()
        plt.ylabel("Sideslip Angle [deg]")
        plt.xlabel("Time since Start Manoeuvre [s]")
        plt.subplot(2, 2, 2)
        plt.plot(TAsym, yAsym[2], label = 'approximate')
        plt.plot(t_measured, generate_data("Body Roll Rate[deg_p_s]"), label = 'measured')
        plt.legend()
        plt.grid()
        plt.ylabel("Roll Rate [deg/s]")
        plt.xlabel("Time since Start Manoeuvre [s]")
        plt.subplot(2, 2, 3)
        plt.plot(TAsym, yAsym[1], label = 'approximate')
        plt.plot(t_measured, generate_data("Roll Angle[deg]"), label = 'measured')
        plt.legend()
        plt.grid()
        plt.ylabel("Roll Angle [deg]")
        plt.xlabel("Time since Start Manoeuvre [s]")
        plt.subplot(2, 2, 4)
        plt.plot(TAsym, yAsym[3], label = 'approximate')
        plt.plot(t_measured, generate_data("Body Yaw Rate[deg_p_s]"), label = 'measured')
        plt.legend()
        plt.grid()
        plt.ylabel("Yaw Rate [deg/s]")
        plt.xlabel("Time since Start Manoeuvre [s]")

def PlotInputs(ShouldPlot, t_min, t_max):
	t_measured = []
	with open(path + "UTC Seconds[sec].csv") as t_data:
		i = 3  # time measurements in 'UTC Seconds [sec]' start at xxx.5 secs
		t_0 = 39568.5  # the initial time as seen in 'UTC Seconds [sec]'
		for t_point in t_data.readlines():
			t_measured.append(float(t_point.strip()) - t_0 - t_min + (i % 10) / 10)
			i += 1
	idx_min = int(t_min * 10)
	idx_max = int(t_max * 10)
	t_measured = t_measured[idx_min:idx_max]

	def generate_data(filename):
		y = []
		with open(path + filename + ".csv") as file:
			for data_point in file.readlines():
				y.append(float(data_point.strip()))

		print("DATA in: ", filename)
		print("Max value: ", max(y[idx_min:idx_max]))
		return y[idx_min:idx_max]

	if ShouldPlot is True:
		plt.figure()
		plt.subplot(1, 3, 1)
		plt.plot(TSym, np.degrees(Uin[:]), label="numerical")
		#plt.plot(t_measured, generate_data('Deflection_of_elevator[deg]'), label ='actual')
		#plt.legend()
		plt.grid()
		plt.ylabel('Elevator deflection [deg]')
		plt.subplot(1, 3, 2)
		plt.plot(TAsym, np.degrees(UinAsym[:,0]), label='numerical')
		#plt.plot(t_measured, generate_data('Deflection of aileron (right wing)[deg]'), label='actual')
		plt.ylabel('Aileron deflection [deg]')
		#plt.legend()
		plt.grid()
		plt.ylabel('Aileron deflection (right wing)[deg]')
		plt.subplot(1, 3, 3)
		plt.plot(TAsym, np.degrees(UinAsym[:, 1]), label='numerical')
		plt.ylabel("Rudder deflection [deg]")
		#plt.plot(t_measured, generate_data('Deflection of rudder[deg]'), label='actual')
		#plt.legend()
		plt.grid()

#PlotFlightData(indexStart, indexEnd, 'True Airspeed[knots]', 'Angle of attack[deg]', 'Pitch Angle[deg]', 'Body Pitch Rate[deg_p_s]')
PrintAB(False)
PrintStabilityDerivatives(False)
PrintEigvals(True)
PlotSym(True, tStart, tEnd)
PlotAsym(True, tStart, tEnd)
PlotInputs(True, tStart, tEnd)

def ShortPeriodOscillation():
    print("Short Period Oscillation")
    sa1 = -2 * mu_c * Ky ** 2 * (Cz_alpha_dot - 2 * mu_c)
    sb1 = -2 * mu_c * Ky ** 2 * Cz_alpha + Cm_q * (Cz_alpha_dot - 2 * mu_c) - Cm_alpha_dot * (Cz_q + 2 * mu_c)
    sc1 = Cz_alpha * Cm_q - Cm_alpha * (Cz_q + 2 * mu_c)
    #Ja echt Ivo wat is dit voor form? #Nou Max s staat voor symmetrich, a,b en c voor de coefficienten in ax^2+bx+c respectievelijk en 1 en 2 staat voor welke eigenvalue het is, logisch toch?
    print("Lambda1 ", (V / chord) * (-sb1 - cmath.sqrt(sb1 ** 2 - 4 * sa1 * sc1)) / (2 * sa1))
    print("Lambda2 ", (V / chord) * (-sb1 + cmath.sqrt(sb1 ** 2 - 4 * sa1 * sc1)) / (2 * sa1))
    print()

def PhugoidMotion():
    print("Phugoid Motion")
    sa2 = 2 * mu_c * ((Cz_alpha * Cm_q) - 2 * mu_c * Cm_alpha)
    sb2 = 2 * mu_c * ((Cx_u * Cm_alpha) - Cm_u * Cx_alpha) + Cm_q * ((Cz_u * Cx_alpha) - (Cx_u * Cz_alpha))
    sc2 = Cz_0 * ((Cm_u * Cz_alpha) - (Cz_u * Cm_alpha))

    lambda21 = (-sb2 - cmath.sqrt(sb2 ** 2 - 4 * sa2 * sc2)) / (2 * sa2)
    lambda22 = (-sb2 + cmath.sqrt(sb2 ** 2 - 4 * sa2 * sc2)) / (2 * sa2)
    print("Lambda1 ", ((V / chord) * lambda21))
    print("Lambda2 ", ((V / chord) * lambda22))
    print()

def HeavilyDampedAperiodicRollingMotion():
    Lambda_b1= V/span * Cl_p/(4*mu_b*Kx**2)
    print("Heavily Damped Aperiodic Rolling Motion:")
    print("Lambda_b1: ", Lambda_b1)
    print()

def DutchRollMotion():
    A = 8*mu_b**2 * Kz**2
    B = -2*mu_b*(Cn_r + 2*Kz**2 *Cy_beta)
    C = 4*mu_b*Cn_beta + Cy_beta*Cn_r
    Lambda1 = V/span * (-B + cmath.sqrt(B ** 2 - 4 * A * C)) / (2 * A)
    Lambda2 = V/span * (-B - cmath.sqrt(B ** 2 - 4 * A * C)) / (2 * A)
    print("Dutch Roll Motion")
    print("Lambda1: ", Lambda1)
    print("Lambda2: ", Lambda2)
    print()

def AperiodicSpiralMotion():
    Lambda_b4 = V/span* (2*CL*(Cl_beta*Cn_r - Cn_beta*Cl_r))/(Cl_p*(Cy_beta*Cn_r + 4*mu_b*Cn_beta) - Cn_p*(Cy_beta*Cl_r + 4*mu_b*Cl_beta))
    print("AperiodicSpiralMotion")
    print("Lambda_b4: ", Lambda_b4)
    print()

def DutchRollMotionAndAperiodicRollingMotion():
    A = 4*mu_b**2 *(Kx**2 * Kz**2 - Kxz**2)
    B = -mu_b*((Cl_r+Cn_p)*Kxz + Cn_r*Kx**2 + Cl_p*Kz**2)
    C = 2*mu_b*(Cl_beta*Kxz+Cn_beta*Kx**2) + 1/4*(Cl_p*Cn_r - Cn_p*Cl_r)
    D = 1/2 * (Cl_beta*Cn_p - Cn_beta*Cl_p)
    Lambda1, Lambda2, Lambda3 = V/span * np.roots([A, B, C, D])

    print("Dutch Roll Motion and Aperiodic Rolling Motion")
    print("Lambda1: ", Lambda1)
    print("Lambda2: ", Lambda2)
    print("Lambda3: ", Lambda3)
    print()


ShortPeriodOscillation()
PhugoidMotion()
HeavilyDampedAperiodicRollingMotion()
DutchRollMotion()
AperiodicSpiralMotion()
DutchRollMotionAndAperiodicRollingMotion()


plt.show()
