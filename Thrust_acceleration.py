# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 18:37:18 2016

@author: Sean Connors
"""

import numpy as np
import matplotlib.pyplot as plt

'''
Net Thrust (F_t) = dm/dt * V_e
where
dm/dt = rate of mass spent per unit time
V_e = effective exhaust velocity 
V_e is calculated from the specific impulse (I_sp), which changes based
on what is used.

'''

#engines burn for around 127 seconds.
#Set force_thrust felt for all of propulsion time
#m_rocket = #something
#m_container = 1000 #starting total mass to be exhausted
#dm_dt = 60  #rate we exhaust the mass per second
#V_e = 453 #speed the mass exits the rocket
#F_t = dm_dt * V_e #total force of thrust per second

def force_gravity(m, x, y):
    '''Calculate the force of gravity on a mass m due to earth.
    
    Parameters:
    
    m : mass of object [kg]
    x : x distance away from the center of earth [m]
    y : y distance away from the center of earth [m]
    
    Returns:
    
    F_g_x, F_g_y: Force on mass m due to gravity in x and y directions respectively [N]'''
    G = 6.6742*10**-11 # gravitational constant, Nm^2/kg^2
    M = 5.9722*10**24 # mass of earth, kg
    # force magnitude
    F_g = G*M*m/(x**2 + y**2)
    
    theta = np.arctan2(y,x)
    F_g_x = F_g * np.cos(theta)
    F_g_y = F_g * np.sin(theta)
    
    return F_g_x, F_g_y

def Force_from_thrust(m, dm_dt, I_p):
    
    G = 6.6742*10**-11 # gravitational constant, Nm^2/kg^2
    M = 5.9722*10**24 # mass of earth, kg
    R = 6371*10**3 # radius of earth, m
    m_container = m
    m_rocket = 350000 #some rocket weight
    t = np.linspace(0, 300, 3000)
    dt = t[1] - t[0]
    dm_dt = dm_dt
    I_p = I_p
    force_vals_x = np.zeros_like(t)
    accel_vals_y = np.zeros_like(t)
    veloc_vals_y = np.zeros_like(t)
    dist_vals_y = np.zeros_like(t)
    #seconds = []
    y_init = R
    x_init = 0.0
    counter = 0
    v_y = 0
    for i in range(3000):
        m_now = m_container - t[i]*dm_dt
        if(m_container - t[i]*dm_dt < 0):
            m_now = 0
        
        force_gravity_x, force_gravity_y = force_gravity(m_rocket+m_now, x_init, y_init)
        force_y_thrust = I_p * dm_dt * force_gravity_y/(m_rocket+m_now)
        if (m_now == 0):
            force_y_thrust = 0
        accel_y = force_y_thrust/(m_rocket+m_now) - force_gravity_y/(m_rocket+m_now)
        v_y += accel_y*dt
        y_init += v_y*dt
        accel_vals_y[i] = accel_y
        veloc_vals_y[i] = v_y
        dist_vals_y[i] = y_init
    return accel_vals_y, veloc_vals_y, dist_vals_y, t

a_y, v_y, d_y, t = Force_from_thrust(1650000.0, 13000.0, 453.0)
plt.plot(t, a_y)
plt.title('acceleration')
plt.show()
plt.plot(t, v_y)
plt.title('velocity')
plt.show()
plt.plot(t, d_y)
plt.title('distance')
plt.show()
print d_y[-1] - d_y[0]