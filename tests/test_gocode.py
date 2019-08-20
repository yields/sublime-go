
import go.gocode as gocode

def test_parse_builtin_const():
  completion = gocode.parse({
    'package': '',
    'class': 'const',
    'name': 'iota',
    'type': '',
  })
  assert completion == ['C・iota', 'iota']

def test_parse_builtin_func():
  completion = gocode.parse({
    'package': '',
    'class': 'func',
    'name': 'real',
    'type': 'func(complex)',
  })
  assert completion == ['ƒ・real(complex) \t\t-> ()', 'real(${1:complex})']

def test_parse_builtin_type():
  completion = gocode.parse({
    'package': '',
    'class': 'type',
    'name': 'rune',
    'type': 'built-in'
  })
  assert completion == ['T・rune', 'rune']

def test_parse_func():
  completion = gocode.parse({
    'package': 'sort',
    'class': 'func',
    'name': 'Slice',
    'type': 'func(slice interface{}, less func(i, j int) bool)',
  })
  assert completion == [
    'ƒ・Slice(slice interface{}, less func) \t\t-> ()',
    'Slice(${1:slice interface{}}, ${2:less func})',
  ]

def test_parse_slice_args():
  completion = gocode.parse({
    'package': 'sort',
    'class': 'func',
    'name': 'Strings',
    'type': 'func(a []string)',
  })
  assert completion == [
    'ƒ・Strings(a []string) \t\t-> ()',
    'Strings(${1:a []string})',
  ]

def test_parse_args_handles_weird_godoc_output():
  completion = gocode.parse({
    'package': 'sort',
    'class': 'func',
    'name': 'Sort',
    'type': 'func(data !sort!sort.Interface)',
  })
  assert completion == [
    'ƒ・Sort(data sort.Interface) \t\t-> ()',
    'Sort(${1:data sort.Interface})',
  ]

def test_parse_func_args():
  (args,_) = gocode.parse_args('func(fn func(int) int) int')
  assert args == [{
    'name': 'fn',
    'type': 'func',
    'args': [{ 'type': 'int', 'name': '' }]
  }]

def test_parse_func_no_args():
  completion = gocode.parse({
    'package': '',
    'class': 'func',
    'name': 'print',
    'type': 'func()'
  })
  assert completion == [
    "ƒ・print() \t\t-> ()",
    'print()$0',
  ]

def test_parse_func_returns():
  completion = gocode.parse({
    'package': '',
    'class': 'func',
    'name': 'sum',
    'type': 'func(...int) int'
  })
  assert completion == [
    "ƒ・sum(...int) \t\t-> (int)",
    'sum(${1:...int})',
  ]

def test_parse_func_multi_returns():
  completion = gocode.parse({
    'package': '',
    'class': 'func',
    'name': 'sum',
    'type': 'func(...int) (int, error)'
  })
  assert completion == [
    "ƒ・sum(...int) \t\t-> (int, error)",
    'sum(${1:...int})',
  ]

def test_parse_func_simple():
  completion = gocode.parse({
    'class': 'func',
    'package': 'net/http',
    'type': 'func(addr string, handler !net/http!http.Handler) error',
    'name': 'ListenAndServe'
  })
  assert completion == [
    'ƒ・ListenAndServe(addr string, handler http.Handler) \t\t-> (error)',
    'ListenAndServe(${1:addr string}, ${2:handler http.Handler})',
  ]
