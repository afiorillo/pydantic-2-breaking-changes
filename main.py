#!/usr/bin/env python

from pydantic import BaseModel

class IntContainer(BaseModel):
    x: int

def main():
    numbers = [
        2**32-1,  # happy 32 bit
        2**32+1,  # sad 32 bit
        2**64-1,  # happy 64 bit
        2**64+1,  # sad 64 bit
        2**128-1,  # happy 128 bit
        2**128+1,  # sad 128 bit
    ]
    
    for num in numbers:
        print(f"{num=}, {type(num)}")
        contained = IntContainer(x=num)
        print(f"{contained=}")
        dumped = contained.json()
        print(f"{dumped=}")
        extracted = contained.x
        print(f"{extracted=}, {type(extracted)}")
        print(f'same? {extracted == num}')
        print('-'*80)
    

if __name__ == '__main__':
    main()
