import os
import numpy as np
import pandas as pd
from collections import deque
import glob
import folium
import random
import string_source as ss

def random_color_code():
	list_A = [ i for i in range(1,10)]
	out = random.sample(list_A, 6)
	out = list(map(str, out))
	return out

def check_the_possible_mapping(df, work_time, day, df_element):
	#index >>  3 7 11 15 19 23


	possible_list = []
	impossible_list = []

	for i in range(len(df)):
		if i%4 == 3:
			
			track_list =[]
			temp_list_1 = df.iloc[i].to_list()
			#print(temp_list_1)
			## 바꿀곳
			left_drive_time_float = float(temp_list_1[1])
			to_dp_time_float = float(temp_list_1[2])
			to_dp_distance = float(temp_list_1[3])

			total_distance_float = float(temp_list_1[4])


			if left_drive_time_float - to_dp_time_float > 0 :
				track_list.append(left_drive_time_float)
				track_list.append(float(work_time) - left_drive_time_float)
				track_list.append(to_dp_time_float)
				track_list.append(to_dp_distance)
				track_list.append(total_distance_float)
				track_list.extend(df.iloc[i-3].to_list()[1:])

				#track_list.extend('DP')
				possible_list.append(track_list)

			else:
				track_list.append(left_drive_time_float)
				track_list.append(float(999))
				track_list.append(to_dp_time_float)
				track_list.append(to_dp_distance)
				track_list.append(total_distance_float)
				track_list.extend(df.iloc[i-3].to_list()[1:])

				#track_list.extend('')
				impossible_list.append(track_list)
							

	result_df = pd.DataFrame(possible_list)
	
	col_name_list = ['left_time','work_time','to_dp_time','to_dp_distance','total_distance']
	for j in range(1,result_df.shape[1]-4):
		col_name_list.append("P"+str(j))


	result_df.columns = col_name_list

	result_df = result_df.sort_values(by=["left_time"], ascending=[True])
	result_df.to_csv("./possible1/"+day+"_"+df_element+"_result.csv",encoding='euc-kr')
	

	result_df_T = result_df.transpose()
	
	T_col_name_list = []

	for k in range(result_df_T.shape[1]):
		T_col_name_list.append("Temp_Route"+str(k))
	
	result_df_T.columns = T_col_name_list
	
	result_df_T.to_csv("./possible1/"+day+"_"+df_element+"_result_T.csv",encoding='euc-kr')

	if impossible_list !=[]:
		im_result_df = pd.DataFrame(impossible_list)
		col_name_im_list = ['left_time','work_time','to_dp_time','to_dp_distance','total_distance']
		#print(im_result_df.shape)
		for j in range(1,im_result_df.shape[1]-4):
			col_name_im_list.append("P"+str(j))
		im_result_df.columns = col_name_im_list	
		im_result_df.to_csv("./possible1/"+day+"_"+df_element+"_im_result.csv",encoding='euc-kr')
		im_result_df_T = im_result_df.transpose()
		
		T_col_name_im_list = []
		for k in range(im_result_df_T.shape[1]):
			T_col_name_im_list.append("Temp_Route"+str(999-k))
					
		im_result_df_T.columns = T_col_name_im_list
		im_result_df_T.to_csv("./possible1/"+day+"_"+df_element+"_im_result_T.csv",encoding='euc-kr')

	else:
		im_result_df_T = pd.DataFrame([])
		im_result_df_T.to_csv("./possible1/"+day+"_"+df_element+"_im_result_T.csv",encoding='euc-kr')	
	
	return result_df_T, im_result_df_T, result_df, im_result_df


def mapping1(T_df, T_im_df, day, df_element ,result_df, im_result_df):
	work_time = 480


	left_time_dict = {}
	work_time_dict = {}
	to_dp_time_dict = {}
	to_dp_distance_dict = {}
	total_distance_dict = {}

	matched_list = []

	T_df = pd.concat([T_df, T_im_df], axis=1)
	#Tmp_df = pd.concat([result_df, im_result_df], axis=1)

	#print(T_df.columns, T_df.iloc[0])

	for col, left in zip(T_df.columns, T_df.iloc[0]):
		left_time_dict[col+"-left"] = left
		#print(col+"-left", left)


	for col, work in zip(T_df.columns, T_df.iloc[1]):
		work_time_dict[col+"-work"] = work
		#print(col+"-work", work)

	for col, to_dp in zip(T_df.columns, T_df.iloc[2]):
		to_dp_time_dict[col] = to_dp

	for col, d_dp in zip(T_df.columns, T_df.iloc[3]):
		to_dp_distance_dict[col] = d_dp

	for col, t_distance in zip(T_df.columns, T_df.iloc[4]):
		total_distance_dict[col] = t_distance

	#work_time_dict = dict(sorted(work_time_dict.items(), key = lambda item: item[1], reverse= False))
	
	visited = [False] * len(T_df.columns)
	

	for l_idx, left in enumerate(T_df.columns):
		for w_idx, work in enumerate(T_df.columns[::-1]):
			left_t = left_time_dict[left+"-left"]
			work_t = work_time_dict[work+"-work"]
			dp_t = to_dp_time_dict[left]
			dp_d = to_dp_distance_dict[left]
			total_d_l = total_distance_dict[left]
			total_d_w = total_distance_dict[work]

			#print(left_t, work_t, left, work)
			
			l_idx = l_idx
			w_idx = len(T_df.columns) -1 - w_idx	 

			if visited[l_idx] ==False and visited[w_idx] ==False:
				if left_t - dp_t > work_t and left != work:
					visited[l_idx] = True
					visited[w_idx] = True

					matched_list.append([ (left_t-work_t-dp_t),  (total_d_l+total_d_w+dp_d), left, work])
	

	for i, v  in enumerate(T_df.columns):
		if visited[i]==False:
			matched_list.append([left_time_dict[v+"-left"] , total_distance_dict[v], v, ""])

	#print(matched_list)
	
	
	map1_df = pd.DataFrame(matched_list, columns = ['Left_Time','total_distance', 'Match-1','Match-2'])


	map1_df.to_csv("./possible1/"+day+"_"+df_element+"_result_Match1.csv",encoding='euc-kr')

	return map1_df

def vlookup_data(map1_df, result_df_T, im_result_df_T, day, df_element):
	
	result_DF = result_df_T.transpose()
	im_result_DF = im_result_df_T.transpose()

	#print(result_DF.head(5))
	#print(im_result_DF.head(5))


	#print(map1_df.columns, result_DF.columns)
	merge1_df = pd.merge(map1_df, result_DF, left_on= 'Match-1', right_index=True, how='inner')
	merge1_df.to_csv("./possible1/"+day+"_"+df_element+"_result_Match1_tmp1.csv",encoding='euc-kr')

	merge1_im_df = pd.merge(map1_df, im_result_DF, left_on='Match-1', right_index=True, how='inner')
	merge1_im_df.to_csv("./possible1/" + day + "_" + df_element + "_result_Match1_tmp1_im.csv", encoding='euc-kr')

	merge2_df = pd.merge(map1_df, result_DF, left_on= 'Match-2', right_index=True, how='left')
	merge2_df.to_csv("./possible1/" + day + "_" + df_element + "_result_Match1_tmp2.csv", encoding='euc-kr')

	merge2_im_df = pd.merge(map1_df, im_result_DF, left_on= 'Match-2', right_index=True, how='left')
	merge2_im_df.to_csv("./possible1/" + day + "_" + df_element + "_result_Match1_tmp2_im.csv", encoding='euc-kr')


	view_list = []
	for m1, m2  in zip(merge1_df['Match-1'].values.tolist(),merge2_df['Match-2'].values.tolist()):
		p1 = merge1_df[merge1_df['Match-1']==m1].values.tolist()[0]
		p2 = merge2_df[merge2_df['Match-2']==m2].values.tolist()
		#print(f'p1 : {len(p1), p1}')
		#print(f'p2 : {len(p2), p2}')
		tmp = []
		if len(p2) >= 0:
			tmp.extend(p1[:9])
			tmp.append('DP')
			a = p1[9:]
			#print(f'a : {a}')
			a = ' '.join(a).split()
			a.append('DP')
			tmp.extend(a)

			w = p2[0][9:]
			try:
				w = ' '.join(w).split()
			except:
				w = []

			if len(w) ==0:
				pass;
			else:
				tmp.extend(w)


		else:
			tmp.extend(p1[:9])
			tmp.append('DP')
			a = p1[9:]
			a = ' '.join(a).split()
			tmp.extend(a)

		if tmp[-1] == 'DP':
			tmp = tmp[:-1]
		view_list.append(tmp)
	max_len1 = max(list(map(len, view_list)))

	view_columns = list(merge1_df.columns[:9])
	#print(f'columns : {view_columns}')

	for i in range(max_len1-9):
		view_columns.append('P'+str(i))

	view_df = pd.DataFrame(view_list, columns=view_columns)
	view_df.to_csv("./possible1/"+day+"_"+df_element+"_result_Match_view.csv",encoding='euc-kr')

	#################

	for m1, m2  in zip(merge1_im_df['Match-1'].values.tolist(),merge2_im_df['Match-2'].values.tolist()):
		ip1 = merge1_im_df[merge1_im_df['Match-1']==m1].values.tolist()[0]
		ip2 = merge2_im_df[merge2_im_df['Match-2']==m2].values.tolist()
		print(f'ip2 : {len(ip2), ip2}')
		itmp = []
		if len(ip2) >=0:

			itmp.extend(ip1[:9])
			itmp.append('DP')

			a = ip1[9:]
			a = ' '.join(a).split()

			a.append('DP')
			itmp.extend(a)


			w = ip2[0][9:]
			try:
				w = ' '.join(w).split()
			except:
				w = []

			if len(w) == 0:
				pass;
			else:
				itmp.extend(w)


		else:
			itmp.extend(ip1[:9])
			itmp.append('DP')

			a = ip1[9:]
			a = ' '.join(a).split()
			itmp.extend(a)

		if itmp[-1] == 'DP':
			itmp = itmp[:-1]

		view_list.append(itmp)

	max_len2 = max(list(map(len, view_list)))

	view_columns = list(merge1_im_df.columns[:9])


	for i in range(max_len2-9):
		view_columns.append('P'+str(i))

	view_df = pd.DataFrame(view_list, columns=view_columns)

	view_df['work_time'] = 480 - view_df['left_time']


	view_df['left_time'] = view_df['Left_Time']
	view_df.drop(['Left_Time','Match-1','Match-2','total_distance_y','to_dp_distance'], axis=1, inplace=True)
	Route_idx = len(view_df['left_time'].values.tolist())

	b = []
	for r in range(Route_idx):
		b.append('Route'+str(r))

	view_df['Route'] = b

	v_c = list(view_df.columns)[:-1]
	vv =['Route']
	vv.extend(v_c)
	view_df = view_df.reindex(columns=vv)

	view_df['work_time'] = 480 - view_df['left_time']




	view_df.to_csv("./possible1/" + day + "_" + df_element + "_result_Match_view_2.csv", encoding='euc-kr')


	return view_df



def location_xy(final_df, location_df, DP_df, day, df_element):
	
	final_df_T = final_df.transpose()
	
	cols_list = []
	for i in range(final_df_T.shape[1]):
		cols_list.append('Mapped_Route'+str(i))
		
	final_df_T.columns = cols_list
	final_df_T.to_csv("./possible1/"+day+"_"+df_element+"_result_mapping.csv",encoding='euc-kr')	

	located_df = location_df[['code', '경도(X좌표)', '위도(Y좌표)']]
	#located_df = pd.DataFrame(located_df, columns=[['code', '경도(X좌표)', '위도(Y좌표)']])

	if not os.path.isdir(df_element):
		os.mkdir(df_element)
	
	y = DP_df.loc[DP_df['DP']==df_element,'Latitude'].values[0]
	x = DP_df.loc[DP_df['DP']==df_element,'Longitude'].values[0]
	

	for i in range(final_df_T.shape[1]):
		index_col = 'Mapped_Route'+str(i)

		final_df_part =  pd.DataFrame(final_df_T[index_col], columns=[index_col])
		#final_df_part = final_df_part.replace(' ',np.NaN)
		final_df_part = final_df_part.dropna(axis=0, inplace =False)
		
		map1_df = pd.merge(final_df_part, located_df, left_on=index_col, right_on='code',  how='left')		
	
		map1_df.loc[map1_df[index_col]== 'DP','경도(X좌표)']=x
		map1_df.loc[map1_df[index_col]== 'DP','위도(Y좌표)']=y
	
		map1_df.to_csv("./"+df_element+"/"+day+"_"+df_element+"_result_map_merge_"+str(i)+".csv",encoding='euc-kr')
	
	return


def dataframe2html(route_list, day, df_element, location):
	#print(route_list)
	col_list = []
	for i in range(1, len(route_list[0])+1):
		col_list.append('P'+str(i))

	df = pd.DataFrame(route_list, columns= col_list)
	df.to_html('./map_test/'+df_element+"/"+day+location+'_route.html',encoding='euc-kr')




def draw_map(df_element, day):
	client_code1 = pd.read_csv(ss.Client_code)
	client_code2 = pd.read_excel(ss.DF_client)
	#print(client_code1.head(5))

	path0 =["map_test","./map_test/"+df_element+"/"]
	
	for p in path0:
		if not os.path.isdir(p):
			os.mkdir(p)


	path ="./"+df_element+"/*"

	file_list = glob.glob(path)
	file_list = [ x for x in file_list if day in x]

	file_list_csv = [file for file in file_list if file.endswith(".csv")]

	df = pd.read_csv(file_list_csv[0], encoding='euc-kr')
	
	y = df.loc[df[df.columns[1]]=="DP",'위도(Y좌표)'].values[0]
	x = df.loc[df[df.columns[1]]=="DP",'경도(X좌표)'].values[0]
	init_xy = [y, x]
	
	MM = folium.Map(location = init_xy, zoom_start=10)

	for i in file_list_csv:
		position_list = []
		position_name = []

		df = pd.read_csv(i, encoding='euc-kr')	
		location = df[df.columns[1]].values.tolist()
		df1 = df.replace(np.NaN, "")
		df1.to_html('./map_test/'+df_element+"/"+day+df.columns[1]+'_detail.html',encoding='euc-kr')		
		
		for idx, p in enumerate(location):
			if idx>=3 :
				if p == 'DP' or df_element in p:
					
					y = df.loc[df[df.columns[1]]==p,'위도(Y좌표)'].values[0]
					x = df.loc[df[df.columns[1]]==p,'경도(X좌표)'].values[0]
					position_list.append([y, x])
					position_name.append(p)			

		m = folium.Map(location = position_list[0], zoom_start=12)
		
		count = 1
		P_list =[]

		p_list = []

		for point in position_name:


			if point != 'DP':

				origin_code = client_code2[client_code2['code'] == point]['code1'].values.tolist()[0]


				real_code = client_code1[client_code1['local_code'] == origin_code]['CUST_NM'].values.tolist()[0]
				p_list.append(real_code)
			else:
				p_list.append(point)

		#print(f'point list : {p_list}')

		color_list = random_color_code()

		color_code = ''.join(color_list)
		color_code = '#' + color_code

		for P,M in zip(position_list, p_list):
			if M !='DP':
				folium.Marker(P, popup=str(count)+"-"+M).add_to(m)
				folium.Marker(P, popup=str(count)+"-"+M).add_to(MM)
			else:
				folium.Marker(P, popup=str(count)+"-"+M, icon=folium.Icon(color='red')).add_to(m)
				folium.Marker(P, popup=str(count)+"-"+M, icon=folium.Icon(color='red')).add_to(MM)
			count+=1		
			P_list.append(M)


		folium.PolyLine(locations = position_list, tooltip='Polyline').add_to(m)
		folium.PolyLine(locations = position_list, tooltip='Polyline', color=color_code).add_to(MM)
		folium.Polygon(locations = position_list, fill=True, tooltip='Polygon' ,color=color_code).add_to(MM)

		#m.add_child(folium.ClickForMarker(popup= 'ClickForMarker'))
		m.save("./map_test/"+df_element+"/"+day+"_"+df.columns[1]+"_map_test.html")
		location_n = df.columns[1]
		dataframe2html([P_list], day, df_element, location_n)

	MM.save("./map_test/"+df_element+"/"+day+"_total_"+"map_test.html")


