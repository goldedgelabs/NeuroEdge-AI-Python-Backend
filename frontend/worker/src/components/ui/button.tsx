'use client';
import React from 'react';
export function Button({children, className='', ...props}: any){
  return <button className={'px-3 py-2 rounded-md bg-ne-primary text-white ' + className} {...props}>{children}</button>;
}
export default Button;
