import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from scipy.optimize import curve_fit
from matplotlib.patches import Ellipse
import matplotlib.lines as Lines

def gaussian(x, a, mu, sigma):
    return a * np.exp(-(x-mu)**2/(2*sigma**2))

# ty = 0 for area in um^2, ty= 1 for major axis in ellipse in um
ty = 1
list_fiber=[]
with open('Fiber results size.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count=0
    for row in csv_reader:
        if line_count==0:
            line_count+=1
        else:
            list_fiber.append(float(row[ty]))
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
            list_accu.append(float(row[ty]))
accu_max = max(list_accu)



list_t0=[]
with open('Results-images-22-50-PVC-as-received-size.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count=0
    for row in csv_reader:
        if line_count==0:
            line_count+=1
        else:
            list_t0.append(float(row[ty]))

t0_max=max(list_t0)
fiber_mean=sum(list_fiber)/len(list_fiber)
print(fiber_mean, 'fib')
accu_mean=sum(list_accu)/len(list_accu)
print(accu_mean, 'accu')
t0_mean=sum(list_t0)/len(list_t0)
print(t0_mean, 't0')


data_list = [list_accu, list_t0, list_fiber]

label_dict = {len(list_accu): '', len(list_t0): '', len(list_fiber): ''}  # not the same length of lists

for val in data_list:
    mu = np.mean(val)
    sigma = np.std(val)
    textstr = '\n'.join((
        r'$\mu=%.2f$' % (mu, ),
        r'$\sigma=%.2f$' % (sigma, ),
        r'n=%.0f' % (len(val),)))
    label_dict[len(val)] = textstr


# xlab = r'Area [$\mu m^2$]'
xlab = r'Major axis, a, of fitted ellipse [$\mu m$]'
ylab = 'Number of particles'

ellipse_title = {'a':'Fitted ellipse of accumulated particles',
              'fib':'Fitted ellipse of particles in the fiber',
              't0': 'Fitted ellipse of PVC particles as received'}

area_title = {'a': 'Area of accumulated particles',
              'fib': 'Area of particles in fiber',
              't0': 'Area of PVC particles as received'}

explain_ell = {'a':0, 'fib': 0, 't0':0}






major = 30
minor = 10


# plot the histograms
fig1, ax1 = plt.subplots()
n1, bins1, _ = ax1.hist(list_accu, bins=30, alpha=0.8)
# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
fig1.suptitle(ellipse_title['a'], fontsize=14)
ax1.set_xlabel(xlab, fontsize=12)
ax1.set_ylabel(ylab, fontsize=12)
max_bin = max(bins1)
max_h = max(n1)
pos = (max_bin - major/2, max_h-minor/2)
explain_ell['a'] = Ellipse(pos, major, minor, facecolor='orange', alpha=0.5)
ax1.add_artist(explain_ell['a'])
line1_major = Lines.Line2D([max_bin-major, max_bin], [max_h - minor/2, max_h - minor/2], color='black')
ax1.add_artist(line1_major)
line1_minor = Lines.Line2D([max_bin - major/2, max_bin - major/2], [max_h, max_h - minor], color='black')
ax1.add_artist(line1_minor)
plt.annotate('a', (max_bin-major/2 -7.5, max_h-minor/2 -2.5))
plt.annotate('b', (max_bin - major/2 + 2, max_h - minor/2+2))



mu1, sigma1 = norm.fit(list_accu)
ax1.axvline(mu1, color='black')
p1 = norm.pdf(bins1, mu1, sigma1)
plt.plot(bins1, p1/p1.sum()*len(list_accu))


# place a text box in upper left in axes coords
ax1.text(0.05, 0.95, label_dict[len(list_accu)], transform=ax1.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

fig2, ax2 = plt.subplots()
major = 50
minor = 12.5

n2, bins2, _ = ax2.hist(list_fiber, 30, alpha=0.8)
# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
fig2.suptitle(ellipse_title['fib'], fontsize=14)
ax2.set_xlabel(xlab, fontsize=12)
ax2.set_ylabel(ylab, fontsize=12)
mu2, sigma2 = norm.fit(list_fiber)
ax2.axvline(mu2, color='black')
p2 = norm.pdf(bins2, mu2, sigma2)
plt.plot(bins2, p2/p2.sum()*len(list_fiber))

max_bin = max(bins2)
max_h = max(n2)
pos = (max_bin - major/2, max_h-minor/2)
explain_ell['fib'] = Ellipse(pos, major, minor, facecolor='orange', alpha=0.5)
ax2.add_artist(explain_ell['fib'])
line2_major = Lines.Line2D([max_bin-major, max_bin], [max_h - minor/2, max_h - minor/2], color='black')
ax2.add_artist(line2_major)
line2_minor = Lines.Line2D([max_bin - major/2, max_bin - major/2], [max_h, max_h - minor], color='black')
ax2.add_artist(line2_minor)
plt.annotate('a', (max_bin-major/2 -7.5, max_h-minor/2 -2.5))
plt.annotate('b', (max_bin - major/2 + 2, max_h - minor/2+2))

# place a text box in upper left in axes coords
ax2.text(0.05, 0.95, label_dict[len(list_fiber)], transform=ax2.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

fig3, ax3 = plt.subplots()

major = 20
minor = 5

n3, bins3, _ = ax3.hist(list_t0, 30, alpha=0.8)
# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
fig3.suptitle(ellipse_title['t0'], fontsize=14)
ax3.set_xlabel(xlab, fontsize=12)
ax3.set_ylabel(ylab, fontsize=12)
mu3, sigma3 = norm.fit(list_t0)
ax3.axvline(mu3, color='black')
p3 = norm.pdf(bins3, mu3, sigma3)
plt.plot(bins3, p3/p3.sum()*len(list_t0))

max_bin = max(bins3)
max_h = max(n3)
pos = (max_bin - major/2, max_h-minor/2)
explain_ell['t0'] = Ellipse(pos, major, minor, facecolor='orange', alpha=0.5)
ax3.add_artist(explain_ell['t0'])
line3_major = Lines.Line2D([max_bin-major, max_bin], [max_h - minor/2, max_h - minor/2], color='black')
ax3.add_artist(line3_major)
line3_minor = Lines.Line2D([max_bin - major/2, max_bin - major/2], [max_h, max_h - minor], color='black')
ax3.add_artist(line3_minor)
plt.annotate('a', (max_bin-major/2 -4, max_h-minor/2 -1))
plt.annotate('b', (max_bin - major/2 + 1, max_h - minor/2+1))

# place a text box in upper left in axes coords
ax3.text(0.05, 0.95, label_dict[len(list_t0)], transform=ax3.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)


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
