import csv

with open('url_list.csv', 'w') as file:
	writer = csv.writer(file)
	for i in range(0, 10000):
		writer.writerow(["https://guide.ethical.org.au/company/?company=" + str(i)])
		