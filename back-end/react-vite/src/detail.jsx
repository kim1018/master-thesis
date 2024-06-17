import React, { useState, useEffect } from 'react'
import { Image, Button } from 'antd'
import { useNavigate, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { LeftOutlined } from '@ant-design/icons'
function Index() {
  const navigate = useNavigate()
  let location = useLocation()
  const { t, i18n } = useTranslation()
  const name = location.state.predicted_text
  const [method, setMethod] = useState('Citrus healthy method')
  const changeLanguage = () => {
    i18n.changeLanguage(i18n.language === 'en' ? 'zh' : 'en')
  }

  useEffect(() => {
    let name_method = location.state.predicted_text + ' method'
    setMethod(name_method)
  }, [name])
  return (
    <div>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
        }}
      >
        <LeftOutlined onClick={() => navigate('/')} />
        <Button size="small" type="primary" onClick={changeLanguage}>
          {i18n.language == 'en' ? 'en' : '中文'}
        </Button>
      </div>
      <div>
        <Image
          src="https://img0.baidu.com/it/u=46322338,1939922915&fm=253&fmt=auto&app=120&f=JPEG?w=500&h=933"
          // style={{ width: '400px', height: '400px' }}
          width={'250px'}
          style={{ height: '300px', marginTop: '20px' }}
        />
      </div>
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          marginTop: '20px',
          fontWeight: 'bold',
        }}
      >
        {t(name)}
      </div>
      <div
        style={{
          display: 'flex',
          justifyContent: 'start',
          marginTop: '20px',
        }}
      >
        {t('resolvent')}:
      </div>
      <div
        style={{
          display: 'flex',
          justifyContent: 'flex-start',
          marginTop: '20px',
          textAlign: 'start',
        }}
      >
        {t(method)}
      </div>
    </div>
  )
}

export default Index
