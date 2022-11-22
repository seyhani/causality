import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('./data_c12_pi_all.csv')

print(df)

plt.plot(df.n, df.N)
plt.title(r'$\frac{N_{Filtered\;CM}}{N_{CM}}$ for $X=C_{1,2}, Y=\Pi_{\{1, \cdots, |E|\}}$')
plt.xlabel(r'$|E|$')
plt.ylabel(r'$N_{Filtered\;CM}\,/\,N_{CM}$')
# plt.show()
plt.savefig('plt_c12_pi_all.jpg', dpi=200)

plt.close()

df = pd.read_csv('./data_c12_pi_half.csv')

print(df)

plt.plot(df.n, df.N)
plt.title(r'$\frac{N_{Filtered\;CM}}{N_{CM}}$ for $X=C_{1,2}, Y=\Pi_{\{1, \cdots, \frac{|E|}{2}\}}$')
plt.xlabel(r'$|E|$')
plt.ylabel(r'$N_{Filtered\;CM}\,/\,N_{CM}$')
# plt.show()
plt.savefig('plt_c12_pi_half.jpg', dpi=200)