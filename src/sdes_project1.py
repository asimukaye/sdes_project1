
# coding: utf-8

# In[114]:

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as my_anim


# In[115]:

def second_order_solver(m, c, l, pos_0, vel_0, tf, dt=0.1):
    s1 = 0.5 * (-c/m + np.sqrt((c/m)**2 - 4.0*g/l + 0.0j))
    s2 = 0.5 * (-c/m - np.sqrt((c/m)**2 - 4.0*g/l + 0.0j))
    a1 = (vel_0 - s2*pos_0)/(s1 - s2)
    a2 = (s1*pos_0 - vel_0)/(s1 - s2)
    t = 0.0
    time = [t]
    pos_array = [pos_0]
    vel_array = [vel_0]
    
    while (t<tf):
        pos = a1*np.exp(s1*t) + a2*np.exp(s2*t)
        vel = a1*s1*np.exp(s1*t) + a2*s2*np.exp(s2*t)
        pos_array.append(pos)
        vel_array.append(vel)
        t += dt
        time.append(t)
    return time, pos_array, vel_array
    


# In[116]:

def pendulum_pos(theta, length):
    r_bob = 0.1
    l = np.linspace(0, length-r_bob, 41)
    string = l*np.exp(1.0j*(theta - np.pi/2.0))
    phi = np.linspace(0.5*np.pi, 2.5*np.pi, 31)
    bob = length*np.exp(1.0j*(theta - np.pi/2.0)) + r_bob*np.exp(1.0j*phi)
    return np.concatenate([string, bob])


# In[117]:

def plot(X, Y, x_name='time (s)', y_name='position', name='position_vs_time'):
    plt.figure()
    plt.plot(X,Y)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.title(name)
    plt.savefig(name+'.png')
    plt.grid()
    #plt.show()
    return 0


# In[118]:

def animator(X,Y):
    fig = plt.figure()
    ax = plt.axes(xlim=(1.5*np.amin(X), 1.5*np.amax(X)), ylim=(1.5*np.amin(Y), 1.5*np.amax(Y)))
    line, = ax.plot([], [], lw=2)
    
    def init():
        line.set_data([],[])
        return line,
    def animate(i):
        x = X[i,:]
        y = Y[i,:]
        #print x,y
        line.set_data(x, y)
        return line,
    
    anim = my_anim.FuncAnimation(fig, animate, init_func=init,
                               frames=len(X), interval=10, blit=True)
    anim.save('final_anim.mp4', fps=10, extra_args=['-vcodec', 'libx264'])
    #plt.show()
    return 0


# In[119]:

def simulate(length=1.0, mass=1.0, damping=0.4, pos_init=1.0, vel_init=0.0, t_sim=20.0):
    global g
    g= 9.8
    t, x, v = second_order_solver(mass, damping, length, pos_init, vel_init, t_sim)
    plot(t, x, y_name='position (m)', name='Angular_Position_vs_time')
    plot(t, v, y_name='velocity(m)', name='Angular_Velocity_vs_time')
    pen = (1.0+1.0j)*np.zeros((len(x), 72))
    #print pendulum_pos(x[0],length)
    for i,angle in enumerate(x):
        pen[i,:] = pendulum_pos(angle,length)
    #print len(pen)
    animator(pen.real, pen.imag)
    return 0


# In[120]:

if __name__=="__main__":
    simulate()


# In[ ]:



