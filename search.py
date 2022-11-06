import os, sys
import pickle

if __name__ == '__main__':
  #connectors = ['"']
  spe = ['/', ' ', '+', '&']
  def merge(a,b):
    ret = []
    i = j = 0
    while len(a) >= i + 1 and len(b) >= j + 1:
        if a[i] <= b[j]:
            ret.append(a[i])
            i += 1
        else:
            ret.append(b[j])
            j += 1
    if len(a) > i:
        ret += a[i:]
    if len(b) > j:
        ret += b[j:]
    return ret

  def search_word(a):
    with open(sys.argv[1]+'/'+'index', "rb") as f:
      index_dict = pickle.load(f)
      ans = []
      if a in index_dict:
        ans = index_dict[a]

    return ans
  def space_search(a,b):
    ans = []
    if a == []:
      return b
    if b == []:
      return a
    ans.append(list(set(a[0]).union(set(b[0]))))
    dic = a[1].copy()
    for j in b[1]:
      if j in a[1]:
        a_merge = a[1][j][0]
        b_merge = b[1][j][0]
        ret0 = merge(a_merge,b_merge)
        a_merge = a[1][j][1]
        b_merge = b[1][j][1]
        ret1 = merge(a_merge,b_merge)
        dic[j] = [ret0,ret1]
      else:
        dic[j] = b[1][j]
    ans.append(dic)
    return ans

  def and_search(a,b):
    ans = []
    if a == []:
      return []
    if b == []:
      return []
    inter = list(set(a[0]).intersection(set(b[0])))
    #print(inter)
    ans.append(inter)
    dic = {}
    for doc_id in inter:
      dic[doc_id] = [merge(a[1][doc_id][0],b[1][doc_id][0]), merge(a[1][doc_id][1],b[1][doc_id][1])]
    
    ans.append(dic)
    return ans

  def plus_search(a,b,dis):
    if dis == 's':
      ans = []
      if a == [] or b == []:
        return ans
      selected = list(set(a[0]).intersection(set(b[0])))
      dic_a = a[1].copy()
      dic_b = b[1].copy()
      doc_id_list = set()
      index_dict = {}
      for doc_id in selected:
        
        for numa in range(len(dic_a[doc_id][0])):
          for numb in range(len(dic_b[doc_id][0])):
            if dic_b[doc_id][0][numb] >= dic_a[doc_id][0][numa] and dic_b[doc_id][1][numb] == dic_a[doc_id][1][numa]:
              doc_id_list.add(doc_id)
              if doc_id not in index_dict:
                index_list = []
                index_list.append([dic_a[doc_id][0][numa],dic_b[doc_id][0][numb]])
                index_list.append([dic_a[doc_id][1][numa],dic_b[doc_id][1][numb]])
                index_dict[doc_id] = index_list
              else:
                if dic_b[doc_id][0][numb] not in index_dict[doc_id][0]:
                  index_dict[doc_id][0].append(dic_b[doc_id][0][numb])
                  index_dict[doc_id][1].append(dic_b[doc_id][1][numb])
                if dic_a[doc_id][0][numa] not in index_dict[doc_id][1]:
                  index_dict[doc_id][0].append(dic_a[doc_id][0][numa])
                  index_dict[doc_id][1].append(dic_a[doc_id][1][numa])
            #if dic_b[doc_id][1][numb] > dic_a[doc_id][1][numa]:
            #  break
      return [list(doc_id_list),index_dict]
    else:
      distance = int(dis)
      ans = []
      if a == [] or b == []:
        return ans
      selected = list(set(a[0]).intersection(set(b[0])))
      dic_a = a[1].copy()
      dic_b = b[1].copy()
      doc_id_list = set()
      index_dict = {}
      for doc_id in selected:
        
        for numa in range(len(dic_a[doc_id][0])):
          for numb in range(len(dic_b[doc_id][0])):
            if dic_b[doc_id][0][numb] >= dic_a[doc_id][0][numa] and dic_b[doc_id][0][numb] <= dic_a[doc_id][0][numa] + distance:
              doc_id_list.add(doc_id)
              if doc_id not in index_dict:
                index_list = []
                index_list.append([dic_a[doc_id][0][numa],dic_b[doc_id][0][numb]])
                index_list.append([dic_a[doc_id][1][numa],dic_b[doc_id][1][numb]])
                index_dict[doc_id] = index_list
              else:
                if dic_b[doc_id][0][numb] not in index_dict[doc_id][0]:
                  index_dict[doc_id][0].append(dic_b[doc_id][0][numb])
                  index_dict[doc_id][1].append(dic_b[doc_id][1][numb])
                if dic_a[doc_id][0][numa] not in index_dict[doc_id][1]:
                  index_dict[doc_id][0].append(dic_a[doc_id][0][numa])
                  index_dict[doc_id][1].append(dic_a[doc_id][1][numa])
            #if dic_b[doc_id][0][numb] > dic_a[doc_id][0][numa] + distance:
            #  break
      return [list(doc_id_list),index_dict]
      
  def slash_search(a,b,dis):
    if dis == 's':
      ans = []
      if a == [] or b == []:
        return ans
      selected = list(set(a[0]).intersection(set(b[0])))
      dic_a = a[1].copy()
      dic_b = b[1].copy()
      doc_id_list = set()
      index_dict = {}
      for doc_id in selected:
        
        for numa in range(len(dic_a[doc_id][0])):
          for numb in range(len(dic_b[doc_id][0])):
            if dic_b[doc_id][1][numb] == dic_a[doc_id][1][numa]:
              doc_id_list.add(doc_id)
              if doc_id not in index_dict:
                index_list = []
                index_list.append([dic_a[doc_id][0][numa],dic_b[doc_id][0][numb]])
                index_list.append([dic_a[doc_id][1][numa],dic_b[doc_id][1][numb]])
                index_dict[doc_id] = index_list
              else:
                if dic_b[doc_id][0][numb] not in index_dict[doc_id][0]:
                  index_dict[doc_id][0].append(dic_b[doc_id][0][numb])
                  index_dict[doc_id][1].append(dic_b[doc_id][1][numb])
                if dic_a[doc_id][0][numa] not in index_dict[doc_id][1]:
                  index_dict[doc_id][0].append(dic_a[doc_id][0][numa])
                  index_dict[doc_id][1].append(dic_a[doc_id][1][numa])
            #if dic_b[doc_id][1][numb] > dic_a[doc_id][1][numa]:
            #  break
      return [list(doc_id_list),index_dict]
    else:
      distance = int(dis)
      ans = []
      if a == [] or b == []:
        return ans
      selected = list(set(a[0]).intersection(set(b[0])))
      dic_a = a[1].copy()
      dic_b = b[1].copy()
      doc_id_list = set()
      index_dict = {}
      for doc_id in selected:
        
        for numa in range(len(dic_a[doc_id][0])):
          for numb in range(len(dic_b[doc_id][0])):
            if dic_b[doc_id][0][numb] >= dic_a[doc_id][0][numa] and dic_b[doc_id][0][numb] <= dic_a[doc_id][0][numa] + distance:
              doc_id_list.add(doc_id)
              if doc_id not in index_dict:
                index_list = []
                index_list.append([dic_a[doc_id][0][numa],dic_b[doc_id][0][numb]])
                index_list.append([dic_a[doc_id][1][numa],dic_b[doc_id][1][numb]])
                index_dict[doc_id] = index_list
              else:
                if dic_b[doc_id][0][numb] not in index_dict[doc_id][0]:
                  index_dict[doc_id][0].append(dic_b[doc_id][0][numb])
                  index_dict[doc_id][1].append(dic_b[doc_id][1][numb])
                if dic_a[doc_id][0][numa] not in index_dict[doc_id][1]:
                  index_dict[doc_id][0].append(dic_a[doc_id][0][numa])
                  index_dict[doc_id][1].append(dic_a[doc_id][1][numa])
            #if dic_b[doc_id][0][numb] > dic_a[doc_id][0][numa] + distance:
            #  break

      for doc_id in selected:
        
        for numb in range(len(dic_b[doc_id][0])):
          for numa in range(len(dic_a[doc_id][0])):
            if dic_a[doc_id][0][numa] >= dic_b[doc_id][0][numb] and dic_a[doc_id][0][numa] <= dic_b[doc_id][0][numb] + distance:
              doc_id_list.add(doc_id)
              if doc_id not in index_dict:
                index_list = []
                index_list.append([dic_b[doc_id][0][numb],dic_a[doc_id][0][numa]])
                index_list.append([dic_b[doc_id][1][numb],dic_a[doc_id][1][numa]])
                index_dict[doc_id] = index_list
              else:
                if dic_b[doc_id][0][numb] not in index_dict[doc_id][0]:
                  index_dict[doc_id][0].append(dic_b[doc_id][0][numb])
                  index_dict[doc_id][1].append(dic_b[doc_id][1][numb])
                if dic_a[doc_id][0][numa] not in index_dict[doc_id][1]:
                  index_dict[doc_id][0].append(dic_a[doc_id][0][numa])
                  index_dict[doc_id][1].append(dic_a[doc_id][1][numa])
            #if dic_a[doc_id][0][numa] > dic_b[doc_id][0][numb] + distance:
            #  break
        #index_dict[doc_id][0] = index_dict[doc_id][0].sort()
        #index_dict[doc_id][1] = index_dict[doc_id][1].sort()
      return [list(doc_id_list),index_dict]

  def trans(item):
    terms_list = []
    for s in item:
      if isinstance(s,str):
        hold = ''
        i = 0
        while i < len(s):
          if s[i] != '+' and s[i] != '/' and s[i] != '&' and s[i] != ' ':
            hold += s[i]
          elif s[i] == '+' and hold != '':
            #a = set()
            #a.add(hold)
            k = i+1
            num = ''
            if s[k] == 's':
              num = 's'
            while s[k] >= '0' and s[k] <= '9':
              num += s[k]
              k += 1
            terms_list.append(search_word(hold))
            terms_list.append(s[i:i+1])
            terms_list.append(num)
            hold = ''
            i += (k-i)
          elif s[i] == '/' and hold != '':
            k = i+1
            num = ''
            if s[k] == 's':
              num = 's'
            while s[k] >= '0' and s[k] <= '9':
              num += s[k]
              k += 1
            terms_list.append(search_word(hold))
            terms_list.append(s[i:i+1])
            terms_list.append(num)
            hold = ''
            i += (k-i)
          elif s[i] != '&' and hold != '':
            terms_list.append(search_word(hold))
            terms_list.append(s[i:i+1])
            hold = ''
          elif s[i] != ' ' and hold != '':
            terms_list.append(search_word(hold))
            terms_list.append(s[i:i+1])
            hold = ''
          i += 1
        if hold != '':
          #print(hold)
          terms_list.append(search_word(hold))
      else:
        terms_list.append(s)
      #print(terms_list)

    '''
    step for space event
    '''
    index = 0
    while ' ' in terms_list:
      if index >= len(terms_list):
        break
      if terms_list[index] == ' ':
        terms_list[index] = space_search(terms_list[index-1],terms_list[index+1])
        del terms_list[index+1]
        del terms_list[index-1]
        index = 0
      index += 1

    '''
    step for plus n event
    '''
    index = 0
    while '+' in terms_list:
      if index >= len(terms_list):
        break
      if terms_list[index] == '+' and terms_list[index+1] != 's':
        terms_list[index] = plus_search(terms_list[index-1],terms_list[index+2],terms_list[index+1])
        del terms_list[index+2]
        del terms_list[index+1]
        del terms_list[index-1]
        index = 0
      index += 1

    '''
    step for / n event
    '''
    index = 0
    while '/' in terms_list:
      if index >= len(terms_list):
        break
      if terms_list[index] == '/' and terms_list[index+1] != 's':
        terms_list[index] = slash_search(terms_list[index-1],terms_list[index+2],terms_list[index+1])
        del terms_list[index+2]
        del terms_list[index+1]
        del terms_list[index-1]
        index = 0
      index += 1

    '''
    step for + s event
    '''
    index = 0
    while '+' in terms_list:
      if index >= len(terms_list):
        break
      if terms_list[index] == '+' and terms_list[index+1] == 's':
        terms_list[index] = plus_search(terms_list[index-1],terms_list[index+2],terms_list[index+1])
        del terms_list[index+2]
        del terms_list[index+1]
        del terms_list[index-1]
        index = 0
      index += 1

    '''
    step for / s event
    '''
    index = 0
    while '/' in terms_list:
      if index >= len(terms_list):
        break
      if terms_list[index] == '/' and terms_list[index+1] == 's':
        terms_list[index] = slash_search(terms_list[index-1],terms_list[index+2],terms_list[index+1])
        del terms_list[index+2]
        del terms_list[index+1]
        del terms_list[index-1]
        index = 0
      index += 1
      
    '''
    step for & event
    '''
    index = 0
    while '&' in terms_list:
      if index >= len(terms_list):
        break
      if terms_list[index] == '&':
        terms_list[index] = and_search(terms_list[index-1],terms_list[index+1])
        del terms_list[index+1]
        del terms_list[index-1]
        index = 0
      index += 1

    return terms_list[0]

  while True:
    try:
      a = input()
      # deal with space
      a_cp = ''
      number = {}
      i = 0
      while i < len(a):
        if a[i] == ' ':
          if a[i+1] == '/' or a[i+1] == '+' or a[i+1] == '&':
            if a[i+1] == '&':
              a_cp += '&'
              i = i+2
            elif a[i+1] != '&' and a[i+2] != 's':
              j = i+2
              n = ''
              while a[j] >= '0' and a[j] <= '9':
                n += a[j]
                j += 1
              a_cp += a[i+1]
              number[len(a_cp)] = n
              a_cp += n
              i = j+1
              continue
            elif a[i+2] == 's':
              a_cp += a[i+1]
              a_cp += 's'
              i = i+4
              continue
          else:
            a_cp += a[i]
        else:
          a_cp += a[i]
        i += 1
      #print(a_cp,number)
      a = a_cp
      a_lis = []
      hold = ''
      for i in range(len(a)):
        if a[i] != '(' and a[i] != ')':
          hold += a[i]
        elif a[i] == '(':
          a_lis.append(hold)
          hold = ''
          a_lis.append('(')
        else:
          a_lis.append(hold)
          hold = ''
          a_lis.append(')')
      if hold != '':
        a_lis.append(hold)
    except EOFError:
      break
    except KeyboardInterrupt:
      break
    #print(a_lis)
    while '(' in a_lis:
      #print(a_lis)
      i = 0
      while i < len(a_lis):
        if a_lis[i] == ')':
          a_lis[i-1] = trans([a_lis[i-1]])
          del a_lis[i]
          del a_lis[i-2]
          break
        i += 1
    #print(a_lis)
    a_lis = trans(a_lis)
    #print(a_lis)
    lans = []
    if a_lis == []:
      continue
    for ele in a_lis[0]:
      lans.append(int(ele))
    lans.sort()
    for num in lans:
      print(num)
  