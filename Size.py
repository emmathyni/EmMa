import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from scipy.optimize import curve_fit

def gaussian(x, a, mu, sigma):
    return a * np.exp(-(x-mu)**2/(2*sigma**2))

# row 0 for area in um^2, row 1 for major axis in ellipse in um
list_fiber=[]
with open('Fiber results size.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count=0
    for row in csv_reader:
        if line_count==0:
            line_count+=1
        else:
            list_fiber.append(float(row[1]))
fiber_max=max(list_fiber)


list_accu=[]
accu_main_axis = []
with open('Accumulated results size.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count=0
    for row in csv_reader:
        if line_count==0:
            line_count+=1
        else:
            list_accu.append(float(row[1]))
accu_max = max(list_accu)



list_t0=[]
with open('Results-images-22-50-PVC-as-received-size.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count=0
    for row in csv_reader:
        if line_count==0:
            line_count+=1
        else:
            list_t0.append(float(row[1]))

t0_max=max(list_t0)
fiber_mean=sum(list_fiber)/len(list_fiber)
print(fiber_mean, 'fib')
accu_mean=sum(list_accu)/len(list_accu)
print(accu_mean, 'accu')
t0_mean=sum(list_t0)/len(list_t0)
print(t0_mean, 't0')


list_of_str = [list_accu, list_t0, list_fiber]

label_dict = {len(list_accu): '', len(list_t0): '', len(list_fiber): ''}  # not the same length of lists

for l in list_of_str:
    mu = np.mean(l)
    sigma = np.std(l)
    textstr = '\n'.join((
        r'$\mu=%.2f$' % (mu, ),
        r'$\sigma=%.2f$' % (sigma, ),
        r'n=%.0f' % (len(l),)))
    label_dict[len(l)] = textstr


# xlab = r'Area [$\mu m^2$]'
xlab = r'Major axis of fitted ellipse [$\mu m$]'
ylab = 'Number of particles'




# plot the histograms
fig1, ax1 = plt.subplots()
_, bins1, _ = ax1.hist(list_accu, bins=30, alpha=0.8)
# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
fig1.suptitle('Fitted ellipse of accumulated particles')
ax1.set_xlabel(xlab)
ax1.set_ylabel(ylab)


mu1, sigma1 = norm.fit(list_accu)
ax1.axvline(mu1, color='black')
p1 = norm.pdf(bins1, mu1, sigma1)
plt.plot(bins1, p1/p1.sum()*len(list_accu))

# place a text box in upper left in axes coords
ax1.text(0.05, 0.95, label_dict[len(list_accu)], transform=ax1.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

fig2, ax2 = plt.subplots()

_, bins2, _ = ax2.hist(list_fiber, 30, alpha=0.8)
# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
fig2.suptitle('Fitted ellipse of particles in the fiber')
ax2.set_xlabel(xlab)
ax2.set_ylabel(ylab)
mu2, sigma2 = norm.fit(list_fiber)
ax2.axvline(mu2, color='black')
p2 = norm.pdf(bins2, mu2, sigma2)
plt.plot(bins2, p2/p2.sum()*len(list_fiber))

# place a text box in upper left in axes coords
ax2.text(0.05, 0.95, label_dict[len(list_fiber)], transform=ax2.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

fig3, ax3 = plt.subplots()

_, bins3, _ = ax3.hist(list_t0, 30, alpha=0.8)
# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
fig3.suptitle('Fitted ellipse of PVC particles as received')
ax3.set_xlabel(xlab)
ax3.set_ylabel(ylab)
mu3, sigma3 = norm.fit(list_t0)
ax3.axvline(mu3, color='black')
p3 = norm.pdf(bins3, mu3, sigma3)
plt.plot(bins3, p3/p3.sum()*len(list_t0))

# place a text box in upper left in axes coords
ax3.text(0.05, 0.95, label_dict[len(list_t0)], transform=ax3.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

print(mu1, sigma1, mu2, sigma2, mu3, sigma3)
plt.show()


exit()







bin_list_fiber = [200*i for i in range(int((fiber_max/200)+1))]
bin_list_accu = [200*i for i in range(int((accu_max/200)+1))]
bin_list_t0 = [200*i for i in range(int((t0_max/200)+1))]
plt.figure()
histo_fiber = plt.hist(list_fiber)
fiber_title="Area of PVC in fiber"
plt.title(fiber_title)
plt.xlabel(r'Area [$\mu$m^2]')
plt.ylabel("Number of particles")

plt.figure()
histo_accu = plt.hist(list_accu)
accu_title="Area of PVC accumulated in bottom of tube"
plt.title(accu_title)
plt.xlabel(r'Area [$\mu$m^2]')
plt.ylabel("Number of particles")
plt.figure()
histo_t0 = plt.hist(list_t0)
t0_title="Area of PVC as received"
plt.title(t0_title)
plt.xlabel(r'Area [$\mu$m^2]')
plt.ylabel("Number of particles")
plt.show()
