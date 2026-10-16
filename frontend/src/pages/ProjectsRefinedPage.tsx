import {useEffect, useState} from 'react'
import {Link} from 'react-router-dom'
import {PageHero} from '../components/common/PageHero'
import {Seo} from '../components/common/Seo'
import {api} from '../services/api'
import type {Project} from '../types'

export function ProjectsRefinedPage() {
  const [projects, setProjects] = useState<Project[]>([])
  useEffect(() => { api.projects().then(setProjects) }, [])

  return <>
    <Seo title="Проекты — КУДЛАЙН" description="Опубликованные проекты ООО «КУДЛАЙН»: металлоконструкции для реализованных объектов."/>
    <PageHero title="Проекты" subtitle="Металлоконструкции КУДЛАЙН в реализованных объектах" crumbs={[{label: 'Проекты'}]}/>
    {projects.length > 0 && <section className="section">
      <div className="shell project-grid">
        {projects.map(project => <Link className="project-card" to={`/projects/${project.slug}`} key={project.slug}>
          {project.cover_image && <img src={project.cover_image} alt={project.title}/>}
          <div><span>{[project.location, project.year].filter(Boolean).join(' · ')}</span><h2>{project.title}</h2><p>{project.short_description}</p></div>
        </Link>)}
      </div>
    </section>}
  </>
}
