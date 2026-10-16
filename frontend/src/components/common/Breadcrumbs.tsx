import {Link} from 'react-router-dom'

export function Breadcrumbs({items}:{items:{label:string; to?:string}[]}) {
  return <nav className="breadcrumbs" aria-label="Хлебные крошки"><Link to="/">Главная</Link>{items.map((item, index)=><span key={`${item.label}-${index}`}>/ {item.to ? <Link to={item.to}>{item.label}</Link> : item.label}</span>)}</nav>
}
