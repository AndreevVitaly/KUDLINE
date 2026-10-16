import {useEffect} from 'react'
import {useLocation} from 'react-router-dom'

export function ScrollToTop() {
  const {pathname} = useLocation()
  useEffect(() => {
    // The two-argument form works in older Chromium builds too. An exception
    // thrown from an effect can otherwise make React unmount the whole app.
    try {
      window.scrollTo(0, 0)
    } catch {
      document.documentElement.scrollTop = 0
      document.body.scrollTop = 0
    }
  }, [pathname])
  return null
}
