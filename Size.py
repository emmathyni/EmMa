import csv
import matplotlib.pyplot as plt
list_fiber=[]
with open('Fibercorr.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count=0
    for row in csv_reader:
        if line_count==0:
            line_count+=1
        else:
            list_fiber.append(float(row[1]))
fiber_max=max(list_fiber)

list_accu=[]
with open('Results-accumulated.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count=0
    for row in csv_reader:
        if line_count==0:
            line_count+=1
        else:
            list_accu.append(float(row[1]))
accu_max=max(list_accu)

list_t0=[]
with open('Results-t0.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count=0
    for row in csv_reader:
        if line_count==0:
            line_count+=1
        else:
            list_t0.append(float(row[1]))
t0_max=max(list_t0)
fiber_mean=sum(list_fiber)/len(list_fiber)
print(fiber_mean)
accu_mean=sum(list_accu)/len(list_accu)
print(accu_mean)
t0_mean=sum(list_t0)/len(list_t0)
print(t0_mean)



bin_list_fiber = [200*i for i in range(int((fiber_max/200)+1))]
bin_list_accu = [200*i for i in range(int((accu_max/200)+1))]
bin_list_t0 = [200*i for i in range(int((t0_max/200)+1))]
plt.figure()
histo_fiber = plt.hist(list_fiber, bins=bin_list_fiber)
fiber_title="Area of PVC in fiber"
plt.title(fiber_title)
plt.xlabel("Area [um^2]")
plt.ylabel("Number of particles")
plt.figure()
histo_accu = plt.hist(list_accu, bins=bin_list_accu)
accu_title="Area of PVC accumulated in bottom of tube"
plt.title(accu_title)
plt.xlabel("Area [um^2]")
plt.ylabel("Number of particles")
plt.figure()
histo_t0 = plt.hist(list_t0, bins=bin_list_t0)
t0_title="Area of PVC as received"
plt.title(t0_title)
plt.xlabel("Area [um^2]")
plt.ylabel("Number of particles")
plt.show()
