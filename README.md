# Does Pydantic2 handle big integers nicely?

No.

## Big Integers in Python.

Python handles arbitrarily large integers behind the scenes.
This has been the case for over 20 years, see [PEP 237](https://peps.python.org/pep-0237/) for details.

This means that in a Python program, you can happily accept integers of any size you like without overflows.

```python
>>> x = 2**128 + 1
>>> x
340282366920938463463374607431768211457
>>> type(x)
int
```

## Big Integers in Rust.

Rust actually cares about types, and this kind of magic is anathema to the language.
See [here](https://doc.rust-lang.org/book/ch03-02-data-types.html) for actual details.

## Big Integers in Python, with Pydantic v2.

This repository contains an example showing the behavior of wrapping such large integers using the new Pydantic v2, which uses a Rust core.
In particular...

```bash
$ python main.py
num=4294967295, <class 'int'>
contained=IntContainer(x=4294967295)
dumped='{"x":4294967295}'
extracted=4294967295, <class 'int'>
same? True
--------------------------------------------------------------------------------
num=4294967297, <class 'int'>
contained=IntContainer(x=4294967297)
dumped='{"x":4294967297}'
extracted=4294967297, <class 'int'>
same? True
--------------------------------------------------------------------------------
num=18446744073709551615, <class 'int'>
contained=IntContainer(x=9223372036854775807)
dumped='{"x":9223372036854775807}'
extracted=9223372036854775807, <class 'int'>
same? False
--------------------------------------------------------------------------------
num=18446744073709551617, <class 'int'>
contained=IntContainer(x=9223372036854775807)
dumped='{"x":9223372036854775807}'
extracted=9223372036854775807, <class 'int'>
same? False
--------------------------------------------------------------------------------
num=340282366920938463463374607431768211455, <class 'int'>
contained=IntContainer(x=9223372036854775807)
dumped='{"x":9223372036854775807}'
extracted=9223372036854775807, <class 'int'>
same? False
--------------------------------------------------------------------------------
num=340282366920938463463374607431768211457, <class 'int'>
contained=IntContainer(x=9223372036854775807)
dumped='{"x":9223372036854775807}'
extracted=9223372036854775807, <class 'int'>
same? False
--------------------------------------------------------------------------------
```

As you can see, large integers get truncated to `9223372036854775807`.
So if your system currently behaves by allowing numbers of arbitrary size (as Python does by default), and you use Pydantic, then you can expect Pydantic v2 to introduce a new maximum integer size.

## Big Integers in Python, with Pydantic v1

Running the same example with the v1 Pydantic has a different behavior.
In particular, the number is not truncated.
This is not really that surprising, since Pydantic 1 is all Python, but it is a breaking change and worth noticing.

```bash
$ python main.py 
num=4294967295, <class 'int'>
contained=IntContainer(x=4294967295)
dumped='{"x": 4294967295}'
extracted=4294967295, <class 'int'>
same? True
--------------------------------------------------------------------------------
num=4294967297, <class 'int'>
contained=IntContainer(x=4294967297)
dumped='{"x": 4294967297}'
extracted=4294967297, <class 'int'>
same? True
--------------------------------------------------------------------------------
num=18446744073709551615, <class 'int'>
contained=IntContainer(x=18446744073709551615)
dumped='{"x": 18446744073709551615}'
extracted=18446744073709551615, <class 'int'>
same? True
--------------------------------------------------------------------------------
num=18446744073709551617, <class 'int'>
contained=IntContainer(x=18446744073709551617)
dumped='{"x": 18446744073709551617}'
extracted=18446744073709551617, <class 'int'>
same? True
--------------------------------------------------------------------------------
num=340282366920938463463374607431768211455, <class 'int'>
contained=IntContainer(x=340282366920938463463374607431768211455)
dumped='{"x": 340282366920938463463374607431768211455}'
extracted=340282366920938463463374607431768211455, <class 'int'>
same? True
--------------------------------------------------------------------------------
num=340282366920938463463374607431768211457, <class 'int'>
contained=IntContainer(x=340282366920938463463374607431768211457)
dumped='{"x": 340282366920938463463374607431768211457}'
extracted=340282366920938463463374607431768211457, <class 'int'>
same? True
--------------------------------------------------------------------------------
```