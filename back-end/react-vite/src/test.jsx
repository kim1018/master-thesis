import React, { useState } from 'react'

function Index() {
  const [imageFile, setImageFile] = useState('111222')

  return <div>{imageFile}</div>
}

export default Index
