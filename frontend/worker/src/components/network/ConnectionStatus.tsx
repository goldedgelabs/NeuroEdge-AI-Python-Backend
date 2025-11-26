'use client';
import React from 'react';
import NetworkDots from './NetworkDots';

export default function ConnectionStatus(){ return (<div className='flex items-center gap-2'><NetworkDots/><span className='text-sm'>Connection</span></div>); }
