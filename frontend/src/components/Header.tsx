import {useState} from 'react'
import {LogIn, Menu, UserRound, X} from 'lucide-react'
import {NavLink} from 'react-router-dom'
import {Logo} from './Logo'
const items = [['Главная','/'],['О компании','/about'],['Услуги','/services'],['Производство','/production'],['Проекты','/projects'],['Преимущества','/advantages'],['Контакты','/contacts']]
export function Header(){
  const [open,setOpen]=useState(false)
  return <header className="header"><div className="shell header-inner"><Logo/><nav className={open?'nav open':'nav'} aria-label="Основная навигация">{items.map(([label,to])=><NavLink key={to} to={to} end={to==='/'} onClick={()=>setOpen(false)}>{label}</NavLink>)}<NavLink className="button ghost button-small mobile-cta staff-login" to="/client/" onClick={()=>setOpen(false)}><UserRound/>Клиентам</NavLink><NavLink className="button ghost button-small mobile-cta staff-login" to="/workspace/" onClick={()=>setOpen(false)}><LogIn/>Сотрудникам</NavLink><NavLink className="button button-small mobile-cta" to="/request" onClick={()=>setOpen(false)}>Оставить заявку</NavLink></nav><div className="header-actions"><NavLink className="button ghost button-small staff-login" to="/client/" aria-label="Вход в личный кабинет клиента"><UserRound/>Клиентам</NavLink><NavLink className="button ghost button-small staff-login" to="/workspace/" aria-label="Вход в рабочее место сотрудников"><LogIn/>Сотрудникам</NavLink><NavLink className="button button-small" to="/request">Оставить заявку</NavLink></div><button className="menu" onClick={()=>setOpen(!open)} aria-label={open?'Закрыть меню':'Открыть меню'} aria-expanded={open}>{open?<X/>:<Menu/>}</button></div></header>
}

