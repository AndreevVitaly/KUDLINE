import {useEffect, useState} from 'react'
import {Outlet} from 'react-router-dom'
import {Header} from '../Header'
import {Footer} from '../Footer'
import {ScrollToTop} from './ScrollToTop'
import {api, fallbackContact} from '../../services/api'
import type {Contact} from '../../types'

export function Layout() {
  const [contact, setContact] = useState<Contact>(fallbackContact)
  useEffect(() => { api.contacts().then(setContact) }, [])
  return <><ScrollToTop/><Header/><main><Outlet/></main><Footer contact={contact}/></>
}
