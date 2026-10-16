import type {Contact} from '../types'
import {Link} from 'react-router-dom'
import {Logo} from './Logo'
export function Footer({contact}:{contact:Contact}){return <footer className="footer"><div className="shell footer-grid"><div><Logo/><p className="muted">Производство и монтаж металлоконструкций по всей России.</p></div><div><h3>Навигация</h3><Link to="/about">О компании</Link><Link to="/services">Услуги</Link><Link to="/projects">Проекты</Link></div><div><h3>Контакты</h3><a href={`tel:${contact.phone.replace(/\D/g,'')}`}>{contact.phone}</a><a href={`mailto:${contact.email}`}>{contact.email}</a><span>{contact.address}</span></div><div><h3>Информация</h3><Link to="/privacy">Политика конфиденциальности</Link><Link to="/requisites">Реквизиты</Link></div></div><div className="shell footer-bottom"><span>© {new Date().getFullYear()} ООО «КУДЛАЙН»</span><span>Сделано для точной инженерной работы</span></div></footer>}

