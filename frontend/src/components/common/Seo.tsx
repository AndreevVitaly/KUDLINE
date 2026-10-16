import {useEffect} from 'react'

export function Seo({title, description}:{title:string; description:string}) {
  useEffect(() => {
    document.title = title
    const setMeta = (selector:string, attr:string, value:string) => {
      const element = document.querySelector<HTMLMetaElement>(selector)
      if (element) element.content = value
    }
    setMeta('meta[name="description"]', 'content', description)
    setMeta('meta[property="og:title"]', 'content', title)
    setMeta('meta[property="og:description"]', 'content', description)
  }, [title, description])
  return null
}
