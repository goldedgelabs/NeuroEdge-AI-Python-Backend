'use client';
import React from 'react';
export function Badge({children, className=''}: any){
  return <span className={'px-2 py-1 text-xs rounded-full bg-gray-200 '+className}>{children}</span>;
}
export default Badge;
