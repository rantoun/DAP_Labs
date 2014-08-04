import json
import sys
import re
import urllib
from collections import OrderedDict
from bs4 import BeautifulSoup

def contractAsJson(filename):
  url_file = filename
  jsonQuoteData_dict = {}
  page_cont = urllib.urlopen(url_file).read()

  soup = BeautifulSoup(page_cont)

  # Buidling JSON dictionary and its keys
  jsonQuoteData_dict['dateUrls'] = []
  optionTable = []
  optionQuotes = {}

  # RegExs for parsing
  dateurl_regex = re.compile(r'/q/o[p|s]\?s=\S\S?\S?\S?\S?&m=\d{4}-\d{2}[-\d{2}]?')
  stock_symbol_regex = re.compile(r'\((\S+?)\)')
  stock_regex = re.compile(r'^([A-Z][A-Z]?[A-Z]?[A-Z]?[A-Z]?)\d{6}')
  type_regex = re.compile(r'^[A-Z][A-Z]?[A-Z]?[A-Z]?[A-Z]?\d?\d{6}([C|P])')
  optQuoteDate_regex = re.compile(r'^[A-Z][A-Z]?[A-Z]?[A-Z]?[A-Z]?(\d?\d{6})')

  stock_symbol = [re.findall(stock_symbol_regex,str(x.text)) for x in soup.findAll('h2') if re.search(stock_symbol_regex,x.text)]
          
  currPrice_id = "yfs_l84_"+str(stock_symbol[0][0]).lower()
  jsonQuoteData_dict['currPrice'] = [float(x.text) for x in soup.findAll('span',attrs={'id': currPrice_id})][0]

  # Get dateurl, append to yahoo finance
  for link in soup.find_all('a'):
      if re.search(dateurl_regex, link.get('href')):
          x = str(re.sub(r'(&)(m)',r'\1amp;\2',str(link.get('href'))))
          jsonQuoteData_dict['dateUrls'].append("http://finance.yahoo.com"+ x)

  # Get Column headers and append to optionTable
  [optionTable.append(str(x.text)) for x in soup.findAll('tr',attrs={'valign': 'top'})[2].findAll('th',attrs={'class': "yfnc_tablehead1"})]

  # Get all call and put options (yellow and white rows)
  call_opts = [str(x.text) for x in soup.findAll('tr',attrs={'valign': 'top'})[2].findAll('td',attrs={'class': "yfnc_h"})]
  call_opts2 = [str(x.text) for x in soup.findAll('tr',attrs={'valign': 'top'})[2].findAll('td',attrs={'class': "yfnc_tabledata1"})]
  put_opts = [str(x.text) for x in soup.findAll('tr',attrs={'valign': 'top'})[4].findAll('td',attrs={'class': "yfnc_h"})]
  put_opts2 = [str(x.text) for x in soup.findAll('tr',attrs={'valign': 'top'})[4].findAll('td',attrs={'class': "yfnc_tabledata1"})]
  call_opts.extend(call_opts2)
  call_opts.extend(put_opts2)
  call_opts.extend(put_opts)
  all_opts = call_opts
  
  count = 0
  counts = []

  for x in range(len(all_opts)):
    if (x%8) == 0:
      count += 1
      counts.append(count)
  optionQuotes['Counter'] = counts

  for x in range(len(optionTable)):
      vals_list = [str(all_opts[y]) for y in range(len(all_opts)) if (y % 8) == x]
      optionQuotes[optionTable[x]] = vals_list

  symbol_vals = [sym for sym in optionQuotes['Symbol']]

  optionQuotes['Symbol'] = [re.findall(stock_regex,sym)[0] for sym in symbol_vals]
  optionQuotes['Type'] = [re.findall(type_regex,sym)[0] for sym in symbol_vals]
  optionQuotes['Date'] = [re.findall(optQuoteDate_regex,sym)[0] for sym in symbol_vals]

  list_of_dicts = []

  for i in range(len(optionQuotes['Strike'])):
      final_dict = {}
      for key in optionQuotes:
          if key == 'Open Int':
              final_dict['Open'] = optionQuotes[key][i]
              if re.search(r',', optionQuotes[key][i]):
                  final_dict['Open'] = re.sub(r',',r'', optionQuotes[key][i])
              final_dict['Open'] = int(final_dict['Open'])
          elif key == 'Chg':
              final_dict['Change'] = optionQuotes['Chg'][i]
          else:
              final_dict[key] = optionQuotes[key][i]
          final_sorted_dict = OrderedDict(sorted(final_dict.items(), key=lambda x: x[0]))
      list_of_dicts.append(final_sorted_dict)
  
  # Sort lists in reverse based on "Open" key, then tiebreak based on table order
  list_of_dicts.sort(lambda x, y: 1 if (x["Open"] < y["Open"]) else -1 if (x["Open"] > y["Open"]) else x["Counter"] < y["Counter"])
  
  for x in list_of_dicts:
    del x['Counter']

  # Convert Open int values back to string and insert commas when necessary
  for option in list_of_dicts:
      option['Open'] = str(option['Open'])
      if len(option['Open']) >= 4 and len(option['Open']) < 10:
          option['Open'] = re.sub(r'(\d?\d?\d)(\d{3})',r'\1,\2', str(option['Open']))
  
  # Set list of dicts to optionQuotes key and sort by alphabetical order
  jsonQuoteData_dict['optionQuotes'] = list_of_dicts
  jsonQuoteData_dict = OrderedDict(sorted(jsonQuoteData_dict.items(), key=lambda x: x[0]))

  jsonQuoteData = json.dumps(jsonQuoteData_dict,indent=4)
  return jsonQuoteData


