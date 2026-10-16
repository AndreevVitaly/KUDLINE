import {useState} from 'react'
import {Menu, X} from 'lucide-react'
import {NavLink} from 'react-router-dom'
import {Logo} from './Logo'
const items = [['Главная','/'],['О компании','/about'],['Услуги','/services'],['Производство','/production'],['Проекты','/projects'],['Преимущества','/advantages'],['Контакты','/contacts']]
export function Header(){
  const [open,setOpen]=useState(false)
  return <header className="header"><div className="shell header-inner"><Logo/><nav className={open?'nav open':'nav'} aria-label="Основная навигация">{items.map(([label,to])=><NavLink key={to} to={to} end={to==='/'} onClick={()=>setOpen(false)}>{label}</NavLink>)}<NavLink className="button button-small mobile-cta" to="/request" onClick={()=>setOpen(false)}>Оставить заявку</NavLink></nav><NavLink className="button button-small desktop-cta" to="/request">Оставить заявку</NavLink><button className="menu" onClick={()=>setOpen(!open)} aria-label="Открыть меню">{open?<X/>:<Menu/>}</button></div></header>
}

