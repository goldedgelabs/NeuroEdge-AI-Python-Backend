'use client';
import React from 'react';
export function Card({children, className='', ...props}: any){
  return <div className={'p-4 bg-ne-card border rounded-md '+className} {...props}>{children}</div>;
}
export default Card;
