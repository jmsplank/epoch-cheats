# epoch-cheats

## Installation
```bash
$ git clone https://github.com/jmsplank/epoch-cheats.git
$ cd epoch-cheats
$ pip install -e .
```

## Usage

### In Command Prompt
```bash
$ epoch-cheats deck eval tests.test_input.deck

begin: constant
   qe  =  1.602e-19
  mu0  =  1.257e-06
   kb  =  1.381e-23
   pi  =  3.140e+00
    g  =  9.810e+00
end: constant
Successfully evaluated tests/test_input.deck
```

### In Python

Will load an `input.deck` file from any location and return the evaluated constants as a `dict`.

---

```python
# Load Imports
from pathlib import Path
from epoch_cheats import get_deck_constants
```

---

```python
# Create Path object pointing to test_input.deck
deck_path = Path("tests/test_input.deck")
# Get the constants block as a dict
constants = get_deck_constants(deck_path)
```

---

```python
# constants contains each constant as a key and its value as a float
constants
```
> Output:
> 
>     {'qe': 1.60217663e-19,
>      'mu0': 1.25663706212e-06,
>      'kb': 1.380649e-23,
>      'pi': 3.14,
>      'g': 9.81}

---

```python
# Extract using the normal syntax
g = constants["g"]
g
```
> Output:
> 
>     9.81

---

```python
# use get_constants_sym() to get a dict with sympy symbols as keys
from epoch_cheats import get_deck_constants_sym
sympy_constants = get_deck_constants_sym(deck_path)
sympy_constants
```
> Output:
> 
>     {qe: 1.60217663e-19,
>      mu0: 1.25663706212e-06,
>      kb: 1.380649e-23,
>      pi: 3.14,
>      g: 9.81}

---

```python
# Access keys using sympy Symbols
from sympy import Symbol
keys = list(sympy_constants.keys())
print("Keys:")
print('\n'.join([f"{k} {type(k)}" for k in keys]))
print("\nGet 'g' using Symbol('g'):")
print(f"g = {sympy_constants[Symbol('g')]}")

```
> Output:
> 
>     Keys:
>     qe  <class 'sympy.core.symbol.Symbol'>
>     mu0 <class 'sympy.core.symbol.Symbol'>
>     kb  <class 'sympy.core.symbol.Symbol'>
>     pi  <class 'sympy.core.symbol.Symbol'>
>     g   <class 'sympy.core.symbol.Symbol'>
>     
>     Get 'g' using Symbol('g'):
>     g = 9.81

---