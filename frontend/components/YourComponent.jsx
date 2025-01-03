import dynamic from 'next/dynamic'

const ComponentWithNoSSR = dynamic(() => import('../components/Component'), {
  ssr: false
})

// Use useEffect for browser-specific code
useEffect(() => {
  // Browser-specific code here
}, []); 