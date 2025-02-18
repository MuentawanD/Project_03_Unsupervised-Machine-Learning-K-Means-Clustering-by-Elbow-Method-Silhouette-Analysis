#!/usr/bin/env python
# coding: utf-8

# # Project : Unsupervised Machine Learning (K-Means Clustering by Elbow Method & Silhouette Analysis)

# ## -----------------------------------------------------------------------------------------------------------

#     เป้าหมาย : เพื่อแบ่งกลุ่มลูกค้าของธุรกิจ โดยหาจำนวนกลุ่ม(Clusters) ที่เหมาะสม 
#                ด้วยวิธี K- Means clustering โดยใช้  Elbow Method & Silhouette Analysis

# ## ------------------------------------------------------------------------------------------------------------

# # 1. Import Llibrary

# In[13]:


get_ipython().system('pip install kneed')
get_ipython().system('pip install yellowbrick')


# In[14]:


# Data
import pandas as pd
import numpy as np

# Data Visualization
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns

# Data preprocessing
from sklearn.preprocessing import StandardScaler

# Clustering Models
from sklearn.cluster import KMeans
from kneed import KneeLocator
from sklearn.metrics import silhouette_score
from yellowbrick.cluster import SilhouetteVisualizer

import warnings 
warnings.filterwarnings("ignore")


# # 2. Load Dataset

#     2.1 โหลด dataset และตั้งชื่อว่า shop_df
#     2.2 เปลี่ยนชื่อ column โดยการแทนที่ช่องว่างทั้งหมดในชื่อคอลัมน์ด้วยเครื่องหมายขีดล่าง (_) 

# In[15]:


shop_df = pd.read_csv(r'C:\Users\muent\Desktop\my project for data analyst\Project-7_Clustering\Dataset\Shop_Customer_Dataset.csv')
shop_df.rename(columns= lambda x: x.replace(" ", "_"), inplace=True)
shop_df


# มารู้จักแต่ละ column ที่อยู่ใน dataset นี้ว่าประกอบด้วยอะไรบ้าง :
# 
# 1. CustomerID: รหัสลูกค้า
# 2. Gender: เพศ
# 3. Age: อายุ
#  4. Annual_Income_(k$): รายได้ต่อปี (หน่วย ดอลล่าห์)
# 5. Spending_Score_(1-100): คะแนนที่ร้านค้าให้กับลูกค้าตามพฤติกรรมและลักษณะการใช้จ่ายของลูกค้า ตั้งแต่คะแนน 1-100 

# # 3. Data Preparation / Data Cleansing

#     3.1 เช็ค datatype
#     3.2 เปลี่ยน datatype ของ CustomerID จาก integer เป็น string
#     3.3 จัดการกับข้อมูลที่หายไป (Missing Value)

# In[16]:


shop_df.dtypes


# In[17]:


shop_df["CustomerID"] = shop_df["CustomerID"].astype(str)
shop_df.dtypes


# In[18]:


shop_df.shape


# In[19]:


shop_df.info()


# In[20]:


shop_df.isnull().sum() #นับค่า Null


# In[21]:


sns.heatmap(shop_df.isnull())
plt.show()


# # 4. พล็อตกราฟ histogram เพื่อดูการกระจายตัวของข้อมูลชุดนี้

# In[22]:


columns = [ 'Age', 'Annual_Income_(k$)', 'Spending_Score_(1-100)'] #เอาเฉพาะ column ตัวเลข

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 3)) # สร้าง subplot figures
sns.set_style()
for i, column in enumerate(columns): # วนลูปเพื่อพล็อตแต่ละคอลัมน์บน subplot ตามลำดับ
    ax = axes[i]
    sns.distplot(shop_df[column], ax=ax)

plt.subplots_adjust(wspace=0.5) # ปรับแต่งระยะห่างระหว่างกราฟ
plt.show()


# In[23]:


shop_df[[ 'Age', 'Annual_Income_(k$)', 'Spending_Score_(1-100)']].describe().round(decimals=2)


#  1. Age : อายุของลูกค้า
#     - ค่า mean > ค่า median จะได้กราฟเบ้ขวา 
#     - ลูกค้ามีหลากหลายวัย
# 2. Annual_Income_(k$) : 
#     - ค่า mean < ค่า median จะได้กราฟเบ้ซ้าย
#     - รายได้ต่อปีของลูกค้าส่วนใหญ่ จะอยู่ระหว่าง 50K- 85K
# 3. Spending_Score_(1-100) :  คะแนนที่ร้านค้าให้กับลูกค้า
#     - ค่า mean = ค่า median กราฟกระจายตัวปกติ Normal distribution
#     - คะแนนที่ร้านค้าให้กับลูกค้าตามพฤติกรรมและลักษณะการใช้จ่ายของลูกค้า ส่วนใหญ่จะอยู่ในช่วง 40 - 60 คะแนน จาก 100 คะแนน

# # 5. พล๊อตกราฟ ดู Outlier

# In[24]:


columns = [ 'Age', 'Annual_Income_(k$)', 'Spending_Score_(1-100)'] 

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 3)) 
for i, column in enumerate(columns): 
    ax = axes[i]
    sns.boxplot(data = shop_df, x = "Gender", y = shop_df[column], ax=ax)

plt.subplots_adjust(wspace=0.5) 
plt.show()


# # 6. พล๊อตกราฟ pairplot เพื่อดูแต่ละความสัมพันธ์ของข้อมูลแต่ละตัว

# In[25]:


sns.pairplot(shop_df, 
             vars = [ 'Age', 'Annual_Income_(k$)', 'Spending_Score_(1-100)'],
             hue = "Gender")
plt.show()


# In[26]:


shop_df.groupby(["Gender"])[[ 'Age', 'Annual_Income_(k$)', 'Spending_Score_(1-100)']].mean()


# # 7. พล๊อตกราฟ Correlation เพื่อดูความสัมพันธ์ของข้อมูล

# In[27]:


shop_df_corr = shop_df[[ 'Age', 'Annual_Income_(k$)', 'Spending_Score_(1-100)']].corr()
shop_df_corr


# In[28]:


sns.heatmap(shop_df_corr, annot= True, cmap = "cividis")
plt.show()


# กราฟนี้คือ **correlation heatmap** ซึ่งแสดงให้เห็นถึงค่าสัมประสิทธิ์สัมพันธ์ระหว่างตัวแปรต่างๆ ได้แก่ **Age, Annual Income, Spending Score**
# 
# **วิธีการอ่านกราฟ:**
# 
# * **ความเข้มของสี:** บอกถึงความสัมพันธ์ที่แข็งแกร่งของตัวแปร ยิ่งสีเหลืองสว่างมากเท่าไหร่ แสดงว่าความสัมพันธ์ทางบวกยิ่งแข็งแกร่ง (Positive Correlation) ในทางกลับกัน สีน้ำเงินเข้ม หมายถึง ความสัมพันธ์ทางลบที่แข็งแกร่ง (Negative Correlation)
# * **ตัวเลข:** ตัวเลขในแต่ละช่องสี่เหลี่ยม แสดงถึง ค่าสัมประสิทธิ์สหสัมพันธ์ (Correlation Coefficient)  ระหว่างตัวแปรทั้งสอง
# 
# **สรุปผลที่สำคัญ:**
# 
# 1. **Age กับ Spending Score (-0.33):** 
#       * มีความสัมพันธ์ทางลบในระดับปานกลาง (Moderate Negative Correlation)  ระหว่าง Age กับ Spending Score นั่นหมายความว่า เมื่ออายุมากขึ้น คะแนนการใช้จ่ายมีแนวโน้มลดลงเล็กน้อย กล่าวโดยสรุป ลูกค้าที่อายุน้อยกว่าอาจมีการใช้จ่ายมากกว่าลูกค้าที่มีอายุ
# 
# 2. **Annual Income กับ Spending Score (0.0099):** 
#     * มีความสัมพันธ์ที่อ่อนมาก (Very Weak Correlation) และใกล้เคียงศูนย์ ซึ่งบ่งบอกว่าแทบจะไม่มีความสัมพันธ์เชิงเส้นตรง (Linear Relationship)  ระหว่างรายได้ต่อปีของลูกค้าและคะแนนการใช้จ่าย  การทราบค่าของตัวแปรหนึ่ง แทบจะไม่ให้ข้อมูลใดๆ เกี่ยวกับตัวแปรอื่นเลย 
# 
# 3. **Age กับ Annual Income (-0.012):** 
#     * มีความสัมพันธ์ทางลบที่อ่อนมาก (Very Weak Negative Correlation) ระหว่างอายุและรายได้ต่อปี  ซึ่งแทบจะไม่มีความสัมพันธ์ ระหว่างตัวแปรทั้งสองในชุดข้อมูลนี้
# 
# ****
# 
# * **ความสัมพันธ์ไม่ได้หมายถึง สาเหตุและผลลัพธ์ (Correlation does not imply causation):** แม้ว่าอาจมีความสัมพันธ์กัน แต่ไม่ได้หมายความว่าตัวแปรหนึ่งเป็น "สาเหตุ" ของการเปลี่ยนแปลงในอีกตัวแปรหนึ่ง อาจมีปัจจัยอื่นๆ ที่มีอิทธิพลต่อตัวแปรทั้งสอง
# * **ความสัมพันธ์เชิงเส้นตรง:** ค่าสัมประสิทธิ์สหสัมพันธ์ใช้วัดความสัมพันธ์ "เชิงเส้นตรง" (Linear Relationship) หากความสัมพันธ์ไม่ใช่เชิงเส้นตรง ค่าสัมประสิทธิ์สหสัมพันธ์อาจไม่สามารถแสดงความสัมพันธ์ได้อย่างถูกต้อง
# 

# # 8. Data Cleaning 

# ## 8.1 Handing Outlier

# * ใช้วิธี Interquartile Range (IQR) : คำนวณ IQR (Q3-Q1) และกำหนดขอบเขต (Q1-1.5IQR) และ (Q3+1.5IQR)
# * Feature ที่มีค่า outlier คือ Annual_Income

# In[29]:


columns = [ 'Age', 'Annual_Income_(k$)', 'Spending_Score_(1-100)'] 

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 3)) 
for i, column in enumerate(columns): 
    ax = axes[i]
    sns.boxplot(data = shop_df, x = "Gender", y = shop_df[column], ax=ax)

fig.suptitle("Before handling outliers", fontsize=16, fontweight='bold')
plt.subplots_adjust(wspace=0.5) 
plt.show()


# In[30]:


#Interquartile Range (IQR) : คำนวณ IQR (Q3-Q1) และกำหนดขอบเขต (Q1-1.5IQR) และ (Q3+1.5IQR) 
# คอลัมน์ที่ต้องการจัดการ outliers
columns_to_handle = [ 'Annual_Income_(k$)']

# จัดการ outliers ใน columns ที่ระบุโดยใช้ IQR
for col in columns_to_handle:
    Q1 = shop_df[col].quantile(0.25)
    Q3 = shop_df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # สร้างเงื่อนไข boolean 
    shop_df01 = (shop_df[col] > lower_bound) & (shop_df[col] < upper_bound)

    # ใช้ loc เพื่อกำหนดค่ากลับให้กับ DataFrame ต้นฉบับ
    shop_df = shop_df.loc[shop_df01]


# In[32]:


columns = [ 'Age', 'Annual_Income_(k$)', 'Spending_Score_(1-100)'] 

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 3)) 
for i, column in enumerate(columns): 
    ax = axes[i]
    sns.boxplot(data = shop_df, x = "Gender", y = shop_df[column], ax=ax)

fig.suptitle("After handling outliers", fontsize=16, fontweight='bold')
plt.subplots_adjust(wspace=0.5) 
plt.show()


# In[31]:


shop_df


# ## 8.2 Handing Null

# In[33]:


shop_df.isnull().sum()


# **ข้อมูลชุดนี้ไม่มีค่า null**

# # 9. Data preparation

# ## 9.1 แบ่งข้อมูลที่ต้องการจัดกลุ่ม

#     - กำหนดให้ X1 คือ ข้อมูลชุดที่ 1 ซึ่งประกอบไปด้วย Annual_Income_(k$) กับ Spending_Score_(1-100) 
#     - กำหนดให้ X2 คือ ข้อมูลชุดที่ 2 ซึ่งประกอบไปด้วย Age กับ Spending_Score_(1-100) 

# In[37]:


# X1 คือ ข้อมูลชุดที่ 1 
X1 = shop_df[['Annual_Income_(k$)', 'Spending_Score_(1-100)']]

# X2 คือ ข้อมูลชุดที่ 2
X2 = shop_df[['Age', 'Spending_Score_(1-100)']]

print(f'ข้อมูลชุดที่ 1 (5 แถวแรก):\n {X1.head(5)}\n')
print(f'ข้อมูลชุดที่ 2 (5 แถวแรก):\n {X2.head(5)}\n')


# ## 9.2  Data standardization ข้อมูล

# In[38]:


scaler = StandardScaler()
#Data standardization ข้อมูลชุดที่ 1
X1_scaled = scaler.fit_transform(X1)

#Data standardization ข้อมูลชุดที่ 2
X2_scaled = scaler.fit_transform(X2)

#numpy.ndarray
#การพิมพ์ 5 แถวแรกของอาร์เรย์ผลลัพธ์ ให้ใช้ slicing อาร์เรย์ด้วย [:5,] แทนการใช้ head(5) ซึ่งจะทำงานกับ DataFrame ของ pandas เท่านั้น

print(f'Data standardization ข้อมูลชุดที่ 1 (5 แถวแรก):\n {X1_scaled[:5,]}\n')
print(f'Data standardization ข้อมูลชุดที่ 2 (5 แถวแรก):\n {X2_scaled[:5,]}\n')  


# # 10. หาจำนวนคลัสเตอร์ (k)ที่เหมาะสม จาก วิธี Elbow Method และ วิธี Silhouette Analysis ร่วมกัน

# **concept:**
#   1. หาจำนวนคลัสเตอร์ (k)ที่เหมาะสม จาก วิธี Elbow Method
#   2. พล็อตกราฟระหว่าง inertia และ k 
#   3. พล็อตเส้นตรงแนวดิ่งตัดจุดหักศอก elbow พอดี จาก library kneed ( from kneed import KneeLocator)
#   4. อ่านค่า k ที่จัดตัดนั้น 
#   5. พล็อตกราฟ Silhouette 
#   6. เลือกค่า optimal k 

# ## 10.1 Elbow Method

# Function find_optimal_k รับพารามิเตอร์ 2 ตัว:
# 
#     X_scaled: ข้อมูลที่จะใช้ในการหาค่า k ที่เหมาะสม
#     title: ชื่อที่จะแสดงในกราฟ

# In[42]:


def find_optimal_k(X_scaled, title):
    inertia = []
    k_range = range(1, 11)

    for k in k_range:
        kmeans = KMeans(n_clusters=k, init='k-means++', random_state=88)
        kmeans.fit(X_scaled)
        inertia.append(kmeans.inertia_)

    # Find the knee (elbow) using kneed library
    kn = KneeLocator(k_range, inertia, curve='convex', direction='decreasing')
    elbow_point = kn.knee

    return k_range, inertia, elbow_point

#พล็อตกราฟ 
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

#พล็อตกราฟของข้อมูลชุดที่ 1 
k_range_X1, inertia_X1, elbow_point_X1 = find_optimal_k(X1_scaled, 'X1_scaled')
ax1.plot(k_range_X1, inertia_X1, marker='o')
ax1.axvline(x=elbow_point_X1, color='r', linestyle='--', label=f'Elbow Point: k={elbow_point_X1}')#พล็อตจุดตัด elbow
ax1.set_title('Elbow Method (X1_scaled)')
ax1.legend()

#พล็อตกราฟของข้อมูลชุดที่ 2
k_range_X2, inertia_X2, elbow_point_X2 = find_optimal_k(X2_scaled, 'X2_scaled')
ax2.plot(k_range_X2, inertia_X2, marker='o')
ax2.axvline(x=elbow_point_X2, color='r', linestyle='--', label=f'Elbow Point: k={elbow_point_X2}') #พล็อตจุดตัด elbow
ax2.set_title('Elbow Method (X2_scaled)')
ax2.legend()

plt.tight_layout() #ปรับขนาดของกราฟให้เหมาะสม
plt.show()


# กราฟนี้ใช้ **Elbow Method** เพื่อหาจำนวนกลุ่ม (k) ที่เหมาะสมในการทำ K-Means Clustering 
# 
# **แกน x:**  จำนวนกลุ่ม (k) ที่ลองกำหนด ตั้งแต่ 1 ถึง 10
# **แกน y:**  Inertia (ค่าเฉื่อย) ซึ่งบ่งบอกถึงความใกล้ชิดของข้อมูลภายในแต่ละกลุ่ม ยิ่ง Inertia ต่ำ ยิ่งข้อมูลภายในกลุ่มใกล้เคียงกันมาก 
# 
# **วิธีการอ่าน:**
# 
# 1. **จุดหักศอก:**  มองหาจุดที่กราฟมีลักษณะ "หักศอก" เหมือนข้อศอก ซึ่งบ่งบอกถึงจุดที่ Inertia เริ่มลดลงน้อยลงอย่างเห็นได้ชัด แสดงว่าการเพิ่มจำนวนกลุ่ม (k) ต่อไป จะไม่ช่วยให้การแบ่งกลุ่มดีขึ้นมากนัก
# 2. **ค่า k ที่เหมาะสม:**  จำนวนกลุ่ม (k) ที่ตรงกับจุดหักศอก ถือเป็นค่าที่เหมาะสมในการทำ K-Means Clustering 
# 
# **ผลลัพธ์จากกราฟ:**
# 
# * **กราฟซ้าย (X1_scaled):**  จุดหักศอกอยู่ที่ k = 5  ซึ่งหมายความว่า การแบ่งข้อมูลใน X1_scaled ออกเป็น 5 กลุ่ม เป็นค่าที่เหมาะสม
# * **กราฟขวา (X2_scaled):** จุดหักศอกอยู่ที่ k = 3 ซึ่งหมายความว่า การแบ่งข้อมูลใน X2_scaled ออกเป็น 3 กลุ่ม เป็นค่าที่เหมาะสม
# 
# **สรุป**  
# **Elbow Method** เป็นเพียงวิธีการหนึ่งในการหาค่า k ที่เหมาะสม อาจใช้ร่วมกับเทคนิคอื่นๆ เช่น **Silhouette Analysis เพื่อยืนยันผลลัพธ์**
# 

# ## 10.2 Silhouette Analysis 

#  **Calculate silhouette score**
#  Function plot_silhouette_coefficients รับพารามิเตอร์ 2 ตัว:
#     X_scaled: ข้อมูลที่จะใช้ในการหาค่า Silhouette Coefficients
#     title: ชื่อที่จะแสดงในกราฟ

# In[40]:


def plot_sil_coef(X_scaled, title):
    sil_coefs = []
    k_range = range(2, 11)
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, init='k-means++', random_state=88)
        kmeans.fit(X_scaled)
        score = silhouette_score(X_scaled, kmeans.labels_, metric='euclidean')
        sil_coefs.append(score)
    
    return k_range, sil_coefs

#พล็อตกราฟ 
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

#พล็อตกราฟของข้อมูลชุดที่ 1 
k_range_X1, sil_coef_X1 = plot_sil_coef(X1_scaled, 'X1_scaled')
ax1.plot(k_range_X1, sil_coef_X1, marker='o')
ax1.set_title('Silhouette Coefficients (X1_scaled)')

#พล็อตกราฟของข้อมูลชุดที่ 2 
k_range_X2, sil_coef_X2 = plot_sil_coef(X2_scaled, 'X2_scaled')
ax2.plot(k_range_X2, sil_coef_X2, marker='o')
ax2.set_title('Silhouette Coefficients (X2_scaled)')

plt.tight_layout() #ปรับขนาดของกราฟให้เหมาะสม
plt.show()


# กราฟนี้แสดง **Silhouette Coefficients** ซึ่งเป็นเมตริกที่ใช้วัดประสิทธิภาพของการทำ K-Means Clustering โดยแสดงให้เห็นว่าข้อมูลภายในแต่ละกลุ่มมีความใกล้เคียงกันมากแค่ไหน และกลุ่มต่างๆ แยกจากกันได้ดีแค่ไหน
# 
# **แกน x:** จำนวนกลุ่ม (k) ที่ลองกำหนด 
# **แกน y:** ค่า Silhouette Coefficient ซึ่งมีค่าอยู่ในช่วง -1 ถึง 1 
# 
# **วิธีการอ่าน:**
# 
# 1. **ค่า Silhouette Coefficient ที่สูง:** บ่งบอกถึงการแบ่งกลุ่มที่ดี 
#     - ค่าเข้าใกล้ 1: ข้อมูลในกลุ่มเดียวกันมีความใกล้เคียงกันมาก และกลุ่มต่างๆ แยกจากกันได้ดี 
#     - ค่าใกล้เคียง 0: ข้อมูลอยู่ใกล้ขอบเขตของกลุ่ม อาจมีการทับซ้อนระหว่างกลุ่ม
#     - ค่าติดลบ:  อาจกำหนดข้อมูลผิดกลุ่ม
# 2. **หาค่า k ที่เหมาะสม:** เลือกค่า k ที่ทำให้ Silhouette Coefficient มีค่าสูงที่สุด 
# 
# **ผลลัพธ์จากกราฟ:**
# 
# * **กราฟซ้าย (X1_scaled):** Silhouette Coefficient มีค่าสูงที่สุดที่ **k = 5 (ประมาณ 0.55)**  และจะเห็นได้ว่า ค่า Silhouette Coefficient มีแนวโน้มลดลงเมื่อ k มากกว่า 5  
# * **กราฟขวา (X2_scaled):**  Silhouette Coefficient มีค่าสูงสุดที่ **k = 5 (ประมาณ 0.46)**  และค่า Silhouette Coefficient  ค่อนข้างคงที่เมื่อ k มากกว่า 5 

# ## 10.3  Silhouette Visualizer ใช้แสดงภาพการกระจายตัวของข้อมูลในแต่ละกลุ่ม (cluster) 

# Function plot_silhouette รับพารามิเตอร์ 2 ตัว:
# 
#     X_scaled: ข้อมูลที่จะใช้ในการพล็อต Silhouette Plot
#     title: ชื่อที่จะแสดงในกราฟ

# In[41]:


def plot_sil_Visualizer(X_scaled, title):
    fig, axes = plt.subplots(1, 4, figsize=(15, 5))
    
    for i, k in enumerate(range(3, 7)):
        model = KMeans(n_clusters=k, init='k-means++', random_state=88)
        visualizer = SilhouetteVisualizer(model, colors='yellowbrick', ax=axes[i])
        visualizer.fit(X_scaled)
        axes[i].set_title(f"Silhouette Plot (k={k})")
        
    fig.suptitle(f"Silhouette Plots for {title}\n --------------------------------------------", fontsize=16)
    plt.tight_layout()
    plt.show()

plot_sil_Visualizer(X1_scaled, 'X1_scaled')
plot_sil_Visualizer(X2_scaled, 'X2_scaled')


# กราฟนี้เรียกว่า **Silhouette Plot** ซึ่งใช้แสดงภาพการกระจายตัวของข้อมูลในแต่ละกลุ่ม (cluster) และช่วยในการประเมินประสิทธิภาพของการทำ K-Means Clustering โดยพิจารณาจากค่า Silhouette Score
# 
# **วิธีการอ่านกราฟ:**
# 
# * **แต่ละกราฟย่อย:** แสดงผลลัพธ์ของ K-Means Clustering ที่ใช้จำนวนกลุ่ม (k) ต่างกัน 
# * **แกน x:** ค่า Silhouette Score ของแต่ละจุดข้อมูล (data point) ซึ่งมีค่าอยู่ในช่วง -1 ถึง 1 
# * **แกน y:** จัดเรียงจุดข้อมูลตามกลุ่ม (cluster) ที่ถูกกำหนด โดยเรียงลำดับตามค่า Silhouette Score จากมากไปน้อยภายในแต่ละกลุ่ม
# * **ความกว้างของแต่ละกลุ่ม:** แสดงจำนวนจุดข้อมูลในกลุ่มนั้นๆ
# * **เส้นประ:** แสดงค่า Silhouette Score เฉลี่ยของการทำ Clustering ในกราฟนั้นๆ
# 
# **สิ่งที่ควรพิจารณาในการเลือกค่า k ที่เหมาะสม:**
# 
# 1. **ค่า Silhouette Score เฉลี่ย:** เลือก k ที่ทำให้ค่า Silhouette Score เฉลี่ยสูงที่สุด
# 2. **รูปร่างของแต่ละกลุ่ม:** แต่ละกลุ่มควรมีรูปร่างที่ค่อนข้างหนาและกว้าง แสดงถึงการกระจายตัวของข้อมูลที่ดีภายในกลุ่ม
# 3. **ความหนาแน่นของแต่ละกลุ่ม:** จุดข้อมูลภายในกลุ่มควรอยู่ใกล้เคียงกัน  และมีช่องว่างระหว่างกลุ่มที่ชัดเจน
# 4. **จุดข้อมูลที่ต่ำกว่าค่าเฉลี่ย:** ควรมีจุดข้อมูลที่ต่ำกว่าค่าเฉลี่ยให้น้อยที่สุด  
# 
# **การวิเคราะห์กราฟ:**
# 
# * **X1_scaled: กลุ่มข้อมูลชุดที่ 1 พิจารณาระหว่าาง Annual Income กับ Spending Score**  
#     * k = 5  ดูเหมือนจะมีค่า Silhouette Score เฉลี่ยสูงที่สุด และรูปร่างของกลุ่มค่อนข้างหนาแน่น  
#     * k = 4  กลุ่มแรกมีขนาดใหญ่กว่ากลุ่มอื่นๆ อย่างเห็นได้ชัด  
# * **X2_scaled: กลุ่มข้อมูลชุดที่ 2 พิจารณาระหว่าาง Age กับ Spending Score**  ** 
#     * k = 4  ดูเหมือนจะมีค่า Silhouette Score เฉลี่ยสูงที่สุด และรูปร่างของกลุ่มค่อนข้างหนาแน่น  
#     * k = 5  กลุ่มแรกมีขนาดใหญ่กว่ากลุ่มอื่นๆ อย่างเห็นได้ชัด  
# 
# **สรุป:**
# 
# * การวิเคราะห์ Silhouette Plot ร่วมกับ Silhouette Coefficient ช่วยให้ตัดสินใจเลือกจำนวนกลุ่ม (k) ที่เหมาะสมในการทำ K-Means Clustering ได้อย่างมีประสิทธิภาพ 
# *  k = 5  ดูเหมือนจะเป็นค่าที่เหมาะสมสำหรับ  X1_scaled  ส่วน  X2_scaled  อาจต้องพิจารณาระหว่าง k = 4 และ k = 5 เพิ่มเติม

# ## 10.4 สรุปค่า K ที่เหมาะสม จาก วิธี Elbow Method และ วิธี Silhouette Analysis , Silhouette Visualizer ร่วมกัน

# ## หาค่า k ที่เหมาะสม
# 
# **💛ข้อมูลชุดที่ 1: X1_scaled**
# 
# * **Elbow Method:** ชี้ให้เห็นว่า k = 5 เป็นจุดหักศอก (Elbow Point)
# * **Silhouette Coefficient:**  แสดงค่าสูงสุดที่ k = 5 เช่นกัน และค่าลดลงเมื่อ k มากกว่า 5 
# * **Silhouette Plot:** k = 5  มีค่า Silhouette Score เฉลี่ยสูง และรูปร่างของกลุ่มมีความหนาแน่นดี  ในขณะที่ k = 4 กลุ่มแรกมีขนาดใหญ่เกินไป
# 
# **สรุปข้อมูลชุดที่ 1:** จากทั้งสามวิธี **ค่า k = 5 เหมาะสมที่สุดสำหรับ X1_scaled** 
# 
#     -------------------------------------------------------------------------------------------------------------
# 
# **💛ข้อมูลชุดที่ 2: X2_scaled**
# 
# * **Elbow Method:** ชี้ให้เห็นว่า k = 3  เป็นจุดหักศอก 
# * **Silhouette Coefficient:** ค่าสูงสุดอยู่ที่ k = 5  แต่ค่าที่ k = 4 และ k = 10 ก็ใกล้เคียงกัน 
# * **Silhouette Plot:** k = 4  มีค่า Silhouette Score เฉลี่ยสูง และรูปร่างของกลุ่มมีความหนาแน่นดี  ในขณะที่ k = 5 กลุ่มแรกมีขนาดใหญ่เกินไป
# 
# **สรุปข้อมูลชุดที่ 2:** Elbow Method ชี้ไปที่ k = 3  แต่ Silhouette Analysis  ชี้ไปที่ k = 4 หรือ k = 5  ในกรณีนี้ ควรให้ความสำคัญกับ Silhouette Analysis มากกว่า เพราะ  Elbow Method อาจไม่ชัดเจนเสมอไป และ k = 4  ดูจะมี Silhouette Plot ที่ดีกว่า k = 5 ในเรื่อง Silhouette Score เฉลี่ยสูง และรูปร่างของกลุ่มมีความหนาแน่นดี ดังนั้น  **k = 4 จึงเหมาะสมที่สุดสำหรับ X2_scaled**
# 
#     -------------------------------------------------------------------------------------------------------------
# 
# **✅สรุปผลการเลือกค่า k:**
# 
# * **X1_scaled:**  k = 5
# * **X2_scaled:** k = 4 
# 

# # 11.  สร้าง Model เพื่อกำหนดเลข cluster ให้แต่ละ data point

# **concept:**
#         1. นำค่า k มาทำการ fit_predict() 
#         2. เก็บค่า cluster labels เพื่อระบุเลขกลุ่มให้แต่ละ data point
#         3. เก็บค่า centroid ของแต่ละกลุ่ม 
#         4. Inverse transform centroid values เปลี่ยนค่า centroid กลับไป fit กับข้อมูลตั้งต้น เพื่อเอาไว้พล็อตกราฟแสดงจุด centroid ของแต่ละคลัสเตอร์

# ฟังก์ชัน cluster_data รับพารามิเตอร์ 3 ตัว:
# 
#     X_scaled: ข้อมูลที่จะใช้ในการทำ Clustering
#     n_clusters: จำนวน cluster ของแต่ละชุดข้อมูล เช่น ข้อมูลชุดที่1 k = 5 , ข้อมูลชุดที่1 k = 4 
#     title: ชื่อที่จะแสดงในผลลัพธ์

# * **11.1 นำค่า k มาทำการ fit_predict()**
# * **11.2 เก็บค่า cluster labels เพื่อระบุเลขกลุ่มให้แต่ละ data point**

# In[44]:


# ข้อมูลชุดที่ 1  X1_scaled, k = 5

kmeans1 = KMeans(n_clusters=5, init='k-means++', random_state=88)
kmeans1.fit_predict(X1_scaled)
cluster_label_X1_scaled = kmeans1.labels_ + 1  # +1 เพื่อให้ cluster label เริ่มจากเลข 1 
print(f'cluster_label_X1_scaled : {cluster_label_X1_scaled}' )


# In[45]:


# ข้อมูลชุดที่ 2  X2_scaled, k = 4

kmeans2 = KMeans(n_clusters=4, init='k-means++', random_state=88)
kmeans2.fit_predict(X2_scaled)
cluster_label_X2_scaled = kmeans2.labels_ + 1  # +1 เพื่อให้ cluster label เริ่มจากเลข 1 
print(f'cluster_label_X2_scaled : {cluster_label_X2_scaled}' )


# * **11.3 เก็บค่า centroid ของแต่ละกลุ่ม**

# In[46]:


# centroids ของข้อมูลชุดที่ 1  X1_scaled, k = 5
centroids_X1_scaled = kmeans1.cluster_centers_
print(f'centroids_X1_scaled: {centroids_X1_scaled}')

# centroids ของข้อมูลชุดที่ 2  X2_scaled, k = 4
centroids_X2_scaled = kmeans2.cluster_centers_
print(f'centroids_X2_scaled: {centroids_X2_scaled}')


# * **11.4 Inverse transform centroid values เปลี่ยนค่า centroid กลับไป fit กับข้อมูลตั้งต้น 
#               เพื่อเอาไว้พล็อตกราฟแสดงจุด centroid ของแต่ละคลัสเตอร์**

# In[47]:


# centroids original ของข้อมูลชุดที่ 1 
scaler = StandardScaler()
X1_scaled = scaler.fit_transform(X1)
centroid_original_X1_scaled = scaler.inverse_transform(kmeans1.cluster_centers_)
print(f'Original Centroids_X1_scaled: {centroid_original_X1_scaled}')

# centroids original ของข้อมูลชุดที่ 2 
scaler = StandardScaler()
X2_scaled = scaler.fit_transform(X2)
centroid_original_X2_scaled = scaler.inverse_transform(kmeans2.cluster_centers_)
print(f'Original Centroids_X2_scaled: {centroid_original_X2_scaled}')


# # 12. เก็บค่า cluster label ใส่ dataframe ที่ชื่อว่า shop_df

# * **12.1 เก็บค่า cluster_label_X1_scaled 
#         ชื่อว่า AnnualIncome_SpendingScore_Cluster**
# 
# * **12.2 เก็บค่า cluster_label_X2_scaled 
#         ชื่อว่า Age_SpendingScore_Cluster**

# In[48]:


shop_df["AnnualIncome_SpendingScore_Cluster"] = cluster_label_X1_scaled 
shop_df["Age_SpendingScore_Cluster"] = cluster_label_X2_scaled 
shop_df


# In[49]:


shop_df.columns

# save file clustering 
shop_df.to_csv('K-Means_Clustering_file.csv')
# # 13. พล็อตกราฟ

# In[61]:


data = shop_df[['Age', 'Annual_Income_(k$)','Spending_Score_(1-100)']]

plt.figure(figsize=(15,5))

#กราฟข้อมูลชุดที่ 1 Annual_Income & Spending_Score
plt.subplot(1,2,1)
sns.scatterplot(x = shop_df["Annual_Income_(k$)"], y = shop_df["Spending_Score_(1-100)"], 
                data = data, s=50, hue=shop_df["AnnualIncome_SpendingScore_Cluster"], palette=sns.color_palette("hls",5))
plt.title("Annual_Income & Spending_Score" , fontsize= 15)

# Plot the centroids
plt.scatter(centroid_original_X1_scaled[:,0], centroid_original_X1_scaled[:,1], c='blue', s=100)

#-----------------------------------

#กราฟข้อมูลชุดที่ 2 Age & Spending_Score
plt.subplot(1,2,2)
sns.scatterplot(x = shop_df["Age"], y = shop_df["Spending_Score_(1-100)"], data = data, s=50, 
                hue=shop_df["Age_SpendingScore_Cluster"], palette=sns.color_palette("husl", 4))
plt.title("Age & Spending_Score", fontsize= 15)
    
#Plot the centroids
plt.scatter(centroid_original_X2_scaled[:,0], centroid_original_X2_scaled[:,1], c='blue', s=100)

plt.show()


# **กราฟแสดงผลการทำ K-Means Clustering โดยแบ่งออกเป็น 2 กราฟย่อย**
# 
# **กราฟซ้าย: Annual Income & Spending Score**
# 
# * แกน x: รายได้ต่อปี (Annual Income)
# * แกน y: คะแนนการใช้จ่าย (Spending Score)
# * สี: แสดงถึงกลุ่ม (cluster) ที่แต่ละจุดข้อมูล (ลูกค้า) ถูกจัดอยู่ใน โดยแบ่งออกเป็น **5 กลุ่ม (ตามค่า k ที่เหมาะสม)**
# * จุดสีน้ำเงิน: แสดงตำแหน่งของจุดศูนย์กลาง (centroid) ของแต่ละกลุ่ม
# 
# **กราฟขวา: Age & Spending Score**
# 
# * แกน x: อายุ (Age)
# * แกน y: คะแนนการใช้จ่าย (Spending Score)
# * สี: แสดงถึงกลุ่ม (cluster) ที่แต่ละจุดข้อมูล (ลูกค้า) ถูกจัดอยู่ใน โดยแบ่งออกเป็น **4 กลุ่ม (ตามค่า k ที่เหมาะสม)**
# *  จุดสีน้ำเงิน: แสดงตำแหน่งของจุดศูนย์กลาง (centroid) ของแต่ละกลุ่ม

# # 14. สรุปผล

# **1. กลุ่มลูกค้าตามรายได้และพฤติกรรมการซื้อ (Annual Income & Spending Score)**
# * **กลุ่ม 1 (Smart Buyer):**  
#    * รายได้สูง แต่คะแนนการใช้จ่ายต่ำ เป็นกลุ่มลูกค้าที่รอบคอบในการใช้จ่าย  ให้ความสำคัญกับข้อมูลสินค้า  เน้นคุณภาพ  และอาจไม่สนใจโปรโมชั่นมากนัก  
#    * **กลยุทธ์**  มุ่งเน้นการให้ข้อมูลสินค้าที่ครบถ้วน  ชูจุดเด่นเรื่องคุณภาพ  และสร้างความน่าเชื่อถือ 
# * **กลุ่ม 2 (Value Seeker):**  
#    * รายได้ปานกลาง  และคะแนนการใช้จ่ายปานกลาง เป็นกลุ่มที่ซื้อสินค้าเป็นประจำ  อาจสนใจสินค้าที่มีความคุ้มค่า  และ โปรโมชั่นที่น่าสนใจ 
#    * **กลยุทธ์**  เน้นการสื่อสารถึงความคุ้มค่าของสินค้า  จัดโปรโมชั่นที่ดึงดูดใจ  และสร้างประสบการณ์ที่ดี 
# * **กลุ่ม 3 (Loyal Customer):** 
#    * รายได้สูง และคะแนนการใช้จ่ายสูง เป็นกลุ่มลูกค้าที่มีกำลังซื้อสูง  และมีความภักดีต่อแบรนด์  
#    * **กลยุทธ์**  รักษาความสัมพันธ์ที่ดี  มอบสิทธิพิเศษ  และสร้างประสบการณ์ที่ดี  เพื่อรักษาฐานลูกค้า
# * **กลุ่ม 4 (Price-Conscious Shopper):** 
#    * รายได้ต่ำ แต่คะแนนการใช้จ่ายสูง  เป็นกลุ่มที่ชอบซื้อสินค้า  แต่มีงบประมาณจำกัด  อาจสนใจสินค้าราคาประหยัด  หรือ โปรโมชั่นลดราคา 
#    * **กลยุทธ์** จัดโปรโมชั่นลดราคา  สินค้าราคาประหยัด  หรือ Cross-selling  เพื่อเพิ่มยอดขาย
# * **กลุ่ม 5 (Bargain Hunter):**  
#    * รายได้ต่ำ และคะแนนการใช้จ่ายต่ำ เป็นกลุ่มที่ซื้อสินค้าไม่บ่อยนัก  อาจสนใจสินค้าราคาถูก  โปรโมชั่นแรงๆ  หรือ สินค้าลดล้างสต๊อก
#    * **กลยุทธ์**  จัดโปรโมชั่นลดราคาแบบจำกัดเวลา  หรือ นำเสนอสินค้าลดล้างสต๊อก  

# **2. กลุ่มลูกค้าตามอายุและพฤติกรรมการซื้อ (Age & Spending Score)**
# 
# * **กลุ่ม 1 (Young Spenders):** 
#     * อายุช่วง 20-40 ปี และมีคะแนนการใช้จ่ายสูง  เป็นกลุ่มวัยรุ่น วัยทำงานตอนต้น  ที่มักใช้จ่ายตามเทรนด์  
#     * **กลยุทธ์**  นำเสนอสินค้าที่ทันสมัย  ใช้สื่อออนไลน์ในการเข้าถึง  และสร้างประสบการณ์ที่น่าตื่นเต้น
# * **กลุ่ม 2 (Conservative Spenders):** 
#     * อายุช่วง 30-70 ปี และมีคะแนนการใช้จ่ายต่ำ  เป็นกลุ่มที่ใช้จ่ายอย่างระมัดระวัง  อาจเน้นคุณภาพ  และ การใช้งานมากกว่า 
#     * **กลยุทธ์**  เน้นคุณภาพและความคุ้มค่า  ให้ข้อมูลสินค้าอย่างละเอียด  และ สร้างความน่าเชื่อถือ
# * **กลุ่ม 3 (Moderate Mature Spenders):**  
#     * อายุช่วง 40-70 ปี และมีคะแนนการใช้จ่ายระดับปานกลาง  เป็นกลุ่มที่มีความมั่นคงในชีวิต  และ ซื้อสินค้าเพื่อตอบสนองความต้องการ
#     * **กลยุทธ์**  นำเสนอสินค้าที่ตอบโจทย์ไลฟ์สไตล์  เน้นคุณภาพ  และ บริการหลังการขาย 
# * **กลุ่ม 4 (Moderate Young Spenders):**  
#     * อายุช่วง 20-40 ปี และมีคะแนนการใช้จ่ายน้อยถึงปานกลาง เป็นกลุ่มที่คล้ายกับกลุ่ม 1 แต่มีกำลังซื้อน้อยกว่า
#     * **กลยุทธ์** นำเสนอสินค้าที่ราคาไม่แพงมาก  มีโปรโมชั่นที่น่าสนใจ  และ เน้นการสื่อสารผ่านช่องทางออนไลน์
# 

# **บทสรุป:**
# 
# * การทำ K-Means Clustering ช่วยให้ธุรกิจสามารถแบ่งกลุ่มลูกค้าที่มีลักษณะคล้ายคลึงกัน ซึ่งนำไปสู่การวางกลยุทธ์ทางการตลาด  การพัฒนาผลิตภัณฑ์  และ การบริการที่ตรงใจลูกค้าแต่ละกลุ่มมากขึ้น
# * การเข้าใจลักษณะและพฤติกรรมของลูกค้าแต่ละกลุ่มอย่างลึกซึ้ง  เป็นกุญแจสำคัญในการสร้างความพึงพอใจ  ความภักดี  และ เพิ่มยอดขายให้กับธุรกิจ
