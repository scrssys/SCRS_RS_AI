import h5py,os
import numpy as np
import matplotlib.pyplot as plt


sampth = r'H:\20200423\train\sample.h5'
f = h5py.File(sampth, 'r')
X = f['X_train'][1]
Y = f['Y_train'][1]
# plt.figure(1)
# plt.subplot(1,2,1)
# plt.imshow(X[:,:,0:3])
# plt.subplot(1,2,2)
# plt.imshow(Y)
# plt.show()
W = f['X_val'][0]
V = f['Y_val'][0]
plt.figure(1)
plt.subplot(1,2,1)
plt.imshow(W[:,:,0:3])
plt.subplot(1,2,2)
plt.imshow(V)
plt.show()
f.close()