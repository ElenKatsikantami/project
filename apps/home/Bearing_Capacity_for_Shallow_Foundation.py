import math
def get_unit_weight(Depth_to_Water,Embedment_depth_of_footings,Unit_Weight,Width_of_foundation):    
    if Depth_to_Water <= Embedment_depth_of_footings:
            Unit_weight_of_subbase = Unit_Weight-9.81
    elif Depth_to_Water <= (Embedment_depth_of_footings+Width_of_foundation):
        Unit_weight_of_subbase = Unit_Weight-9.81 + 9.81 * (Depth_to_Water - Embedment_depth_of_footings)/Width_of_foundation
    else:
        Unit_weight_of_subbase = Unit_Weight
    if Depth_to_Water <= 0 or Depth_to_Water <= Embedment_depth_of_footings:
        Unit_weight_of_surcharge = Unit_Weight-9.81
    elif Depth_to_Water <= (Embedment_depth_of_footings+Width_of_foundation):
        Unit_weight_of_surcharge = Unit_Weight
    else:
        Unit_weight_of_surcharge = 18
    return Unit_weight_of_surcharge,Unit_weight_of_subbase

def get_qallow_Meyerhof(Width_of_foundation,Length_of_foundation,Embedment_depth_of_footings,Depth_to_Water
               ,Friction_Angle,Cohesion,Unit_Weight,alpha,Factor_of_safety):
    # Unit weight:
    Unit_weight_of_surcharge,Unit_weight_of_subbase = get_unit_weight(Depth_to_Water,Embedment_depth_of_footings,Unit_Weight,Width_of_foundation)

    # Bearing Capacity Factors:
    Nq = math.e**(math.pi*math.tan(math.radians(Friction_Angle)))*(math.tan(math.radians(45+(Friction_Angle/2))))**2
    Nc = (Nq-1)*1/math.tan(math.radians(Friction_Angle))
    Ny = 2*(Nq-1)*math.tan(math.radians(Friction_Angle))

    # Shape Factors:
    sq = 1+(Width_of_foundation/Length_of_foundation)*math.sin(math.radians(Friction_Angle))
    sc = (sq*Nq-1)/(Nq-1)
    sy = (1-0.3*(Width_of_foundation/Length_of_foundation))

    # Inclination of the foundation base:
    bq = (1-math.radians(alpha)*math.tan(math.radians(Friction_Angle)))**2 
    bc = bq-(1-bq)/(Nc*math.tan(math.radians(Friction_Angle)))

    # Ultimate Bearing Capacity:

    # Due to Cohesion 
    q1 = Cohesion * Nc * sc * bc
    # Due to Surcharge
    q2 = Embedment_depth_of_footings * Unit_weight_of_surcharge * Nq * sq * bq
    # Due to Unit weight beneath footing
    q3 = 0.5* Width_of_foundation * Unit_weight_of_subbase * Ny * sy * bq

    qult =q1 + q2 + q3

    qallow = qult / Factor_of_safety
    
    return(f"The allowable bearing capacity for the shallow foundation according to Meyerhof is {qallow:.2f} kN/m2")

def get_qallow_Terzaghi(Width_of_foundation,Length_of_foundation,Embedment_depth_of_footings,Depth_to_Water
               ,Friction_Angle,Cohesion,Unit_Weight,alpha,Factor_of_safety):
    # Unit weight:
    Unit_weight_of_surcharge,Unit_weight_of_subbase = get_unit_weight(Depth_to_Water,
                                                                      Embedment_depth_of_footings,
                                                                      Unit_Weight,Width_of_foundation)

    # Bearing Capacity Factors:
    a = math.e**((0.75*math.pi-math.radians(Friction_Angle)/2)*(math.tan(math.radians(Friction_Angle))))
    Nq=a**2/(2*(math.cos(45+0.5*math.radians(Friction_Angle)))**2)
    Nc =(Nq-1)*1/math.tan(math.radians(Friction_Angle))
    Ny = (2*(Nq+1)*math.tan(math.radians(Friction_Angle)))/(1+0.4*math.sin(4*math.radians(Friction_Angle)))

    # Shape Factors:
    if Width_of_foundation == Length_of_foundation:
        sc=1
        sy=1
    else:
        sc=1.3
        sy=0.8
    # Due to Cohesion 
    q1 = Cohesion * Nc * sc
    # Due to Surcharge
    q2 = Embedment_depth_of_footings * Unit_weight_of_surcharge * Nq
    # Due to Unit weight beneath footing
    q3 = 0.5* Width_of_foundation * Unit_weight_of_subbase * Ny * sy

    qult =q1 + q2 + q3

    qallow = qult / Factor_of_safety
    
    return(f"The allowable bearing capacity for the shallow foundation according to Terzaghi is {qallow:.2f} kN/m2")
        

def get_qallow_Hansen(Width_of_foundation,Length_of_foundation,Embedment_depth_of_footings,Depth_to_Water
               ,Friction_Angle,Cohesion,Unit_Weight,alpha,Factor_of_safety,eta,beta):
    # Unit weight:
    Unit_weight_of_surcharge,Unit_weight_of_subbase = get_unit_weight(Depth_to_Water,
                                                                      Embedment_depth_of_footings,
                                                                      Unit_Weight,Width_of_foundation)

    # Bearing Capacity Factors:
    Nq=math.e**(math.pi*math.tan(math.radians(Friction_Angle)))*(math.tan(math.radians(45+(Friction_Angle/2))))**2
    Nc =(Nq-1)*1/math.tan(math.radians(Friction_Angle))
    Ny = 1.5*(Nq-1)*math.tan(math.radians(Friction_Angle))

    # Shape Factors:
    sq=1+(Width_of_foundation/Length_of_foundation)*math.tan(math.radians(Friction_Angle))
    sc=1 + (Nq/Nc)*(Width_of_foundation/Length_of_foundation)
    sy=(1-0.4*(Width_of_foundation/Length_of_foundation))
    
    #depth Factors:
    if Embedment_depth_of_footings/Width_of_foundation <=1:
        k = Embedment_depth_of_footings/Width_of_foundation
    else:
        k = math.atan(Embedment_depth_of_footings/Width_of_foundation)
        
    dq=1+ 2*k*math.tan(math.radians(Friction_Angle))*(1-math.sin(math.radians(Friction_Angle)))**2
    dc=1 +.4*k
    dy=1
    
    # Inclination of the foundation base:
    bq = math.e**(-2 *math.radians(eta) *math.tan(math.radians(Friction_Angle)))
    by = math.e**(-2.7 *math.radians(eta)* math.tan(math.radians(Friction_Angle)))
    bc = 1- math.radians(beta)/147
    #ground Factors:

    gy = gq = (1-.5*math.tan(math.radians(beta)))**5
    gc = 1 - math.radians(beta)/147

    # Ultimate Bearing Capacity:

    # Due to Cohesion 
    q1 = Cohesion * Nc * sc * bc * gc * dc
    # Due to Surcharge
    q2 = Embedment_depth_of_footings * Unit_weight_of_surcharge * Nq * bq* gq * dq
    # Due to Unit weight beneath footing
    q3 = 0.5* Width_of_foundation * Unit_weight_of_subbase * Ny * sy * by * gy * dy

    qult =q1 + q2 + q3

    qallow = qult / Factor_of_safety
    
    return(f"The allowable bearing capacity for the shallow foundation according to Hansen is {qallow:.2f} kN/m2")

def get_qallow_Vesic(Width_of_foundation,Length_of_foundation,Embedment_depth_of_footings,Depth_to_Water
               ,Friction_Angle,Cohesion,Unit_Weight,alpha,Factor_of_safety,eta,beta):
    # Unit weight:
    Unit_weight_of_surcharge,Unit_weight_of_subbase = get_unit_weight(Depth_to_Water,
                                                                      Embedment_depth_of_footings,
                                                                      Unit_Weight,Width_of_foundation)

    # Bearing Capacity Factors:
    Nq=math.e**(math.pi*math.tan(math.radians(Friction_Angle)))*(math.tan(math.radians(45+(Friction_Angle/2))))**2
    Nc =(Nq-1)*1/math.tan(math.radians(Friction_Angle))
    Ny = 2*(Nq-1)*math.tan(math.radians(Friction_Angle))

    # Shape Factors:
    sq=1+(Width_of_foundation/Length_of_foundation)*math.tan(math.radians(Friction_Angle))
    sc=1 + (Nq/Nc)*(Width_of_foundation/Length_of_foundation)
    sy=(1-0.4*(Width_of_foundation/Length_of_foundation))
    
    #depth Factors:
    if Embedment_depth_of_footings/Width_of_foundation <=1:
        k = Embedment_depth_of_footings/Width_of_foundation
    else:
        k = math.atan(Embedment_depth_of_footings/Width_of_foundation)
        
    dq=1+ 2*k*math.tan(math.radians(Friction_Angle))*(1-math.sin(math.radians(Friction_Angle)))**2
    dc=1 +.4*k
    dy=1

    # Inclination of the foundation base:
    bq = by = (1-math.radians(eta)* math.tan(math.radians(Friction_Angle)))**2
    bc = ( 1 - 2*math.radians(beta))/(5.14*math.tan(math.radians(Friction_Angle)))
    #ground Factors:

    gy = gq = (1-.5*math.tan(math.radians(beta)))**2
    gc = 1

    # Ultimate Bearing Capacity:

    # Due to Cohesion 
    q1 = Cohesion * Nc * sc * bc * gc * dc
    # Due to Surcharge
    q2 = Embedment_depth_of_footings * Unit_weight_of_surcharge * Nq * bq* gq * dq
    # Due to Unit weight beneath footing
    q3 = 0.5* Width_of_foundation * Unit_weight_of_subbase * Ny * sy * by * gy * dy

    qult =q1 + q2 + q3

    qallow = qult / Factor_of_safety
    
    return(f"The allowable bearing capacity for the shallow foundation according to Vesic is {qallow:.2f} kN/m2")    
