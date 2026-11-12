import { useEffect, useState } from "react";

import {

  Activity, ArrowDownRight, ArrowRight, ArrowUpRight,

  Bell, BrainCircuit, ChevronLeft, ChevronRight,

  Command, Cpu, Database, Globe2, Layers3, Menu,

  Newspaper, Radio, RefreshCw, Search, Sparkles,

  TrendingUp, X, Zap

} from "lucide-react";

import ArticleReader from "./components/ArticleReader";

import {

  getDashboardStats,

  getArticles,

  getCategories,

  searchArticles,

  getArticlesByCategory

} from "./services/api";



import "./App.css";



function App() {

  const [stats, setStats] = useState(null);

  const [articles, setArticles] = useState([]);

  const [categories, setCategories] = useState([]);

  const [category, setCategory] = useState("All");

  const [keyword, setKeyword] = useState("");

  const [search, setSearch] = useState("");

  const [page, setPage] = useState(1);

  const [totalPages, setTotalPages] = useState(1);

  const [totalResults, setTotalResults] = useState(0);

  const [loading, setLoading] = useState(true);

  const [hasLoadedArticles, setHasLoadedArticles] = useState(false);

  const [error, setError] = useState("");

  const [sidebarOpen, setSidebarOpen] = useState(false);

  const [refreshing, setRefreshing] = useState(false);

  const [selectedArticle, setSelectedArticle] = useState(null);



  const loadStats = async () => {

    const [statsData, categoryData] = await Promise.all([

      getDashboardStats(),

      getCategories()

    ]);

    setStats(statsData);

    setCategories(categoryData.categories || []);

  };





const loadArticles = async () => {

  try {

    setError("");



    let data;



    if (search.trim()) {

      data = await searchArticles(search.trim());



      setArticles(data.articles || []);

      setTotalResults(data.total_results || 0);

      setTotalPages(1);



    } else if (category !== "All") {

      data = await getArticlesByCategory(category);



      setArticles(data.articles || []);

      setTotalResults(data.total_articles || 0);

      setTotalPages(1);



    } else {

      data = await getArticles(page, 10);



      setArticles(data.articles || []);

      setTotalResults(data.total_articles || 0);

      setTotalPages(data.total_pages || 1);

    }



  } catch (err) {

    console.error("Unable to load articles:", err);



    setError(

      "Unable to refresh news. Showing previously loaded articles."

    );



    // Important: Do not clear existing articles here.

  } finally {

    setLoading(false);

    setHasLoadedArticles(true);

  }

 };





  // Load dashboard statistics and categories once when the app starts.
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        await loadStats();
      } catch (err) {
        console.error("Unable to load dashboard statistics:", err);
      }
    };

    fetchDashboardData();
  }, []);

  // Load articles on startup and whenever page/search/category changes.
  useEffect(() => {
    loadArticles();
  }, [page, search, category]);

  const handleSearch = (event) => {

    event.preventDefault();

    setPage(1);

    setCategory("All");

    setSearch(keyword);

  };



  const handleCategory = (value) => {

    setCategory(value);

    setSearch("");

    setKeyword("");

    setPage(1);

  };



  const refreshDashboard = async () => {

    setRefreshing(true);

    try {

      await loadStats();

      await loadArticles();

    } finally {

      setRefreshing(false);

    }

  };



  function formatDate(date) {

  if (!date) return "Recently collected";

  const parsed = new Date(date);

  return Number.isNaN(parsed.getTime())

    ? date

    : parsed.toLocaleDateString("en-IN", {

        day: "numeric",

        month: "short",

        year: "numeric"

      });

}



  const statCards = [

    {

      label: "STORIES INGESTED",

      value: stats?.total_articles ?? "—",

      icon: Newspaper,

      color: "purple",

      detail: "Collected from RSS feeds"

    },

    {

      label: "AI INTERPRETATIONS",

      value: stats?.total_summaries ?? "—",

      icon: BrainCircuit,

      color: "cyan",

      detail: "Processed by Llama 3.2"

    },

    {

      label: "NEWS CATEGORIES",

      value: stats?.total_categories ?? "—",

      icon: Layers3,

      color: "orange",

      detail: "Intelligence streams"

    },

    {

      label: "PENDING STORIES",

      value: stats?.pending_articles ?? "—",

      icon: Activity,

      color: "green",

      detail: `${stats?.failed_articles ?? 0} failed articles`

    }

  ];



  return (

    <div className="app-shell">



      <div className="ambient ambient-one" />

      <div className="ambient ambient-two" />



      {/* SIDEBAR */}

      <aside className={`sidebar ${sidebarOpen ? "sidebar-open" : ""}`}>

        <div className="brand">

          <div className="brand-mark">

            <BrainCircuit size={25} />

          </div>

          <div>

            <h2>NEWSGEN<span>AI</span></h2>

            <small>INTELLIGENCE OS</small>

          </div>

          <button className="mobile-close" onClick={() => setSidebarOpen(false)}>

            <X size={19} />

          </button>

        </div>



        <div className="sidebar-label">WORKSPACE</div>



        <nav className="side-nav">

          <button className="nav-item active">

            <Layers3 size={18} /> Overview

            <span className="nav-indicator" />

          </button>

          <button className="nav-item" onClick={() => handleCategory("All")}>

            <Newspaper size={18} /> News Intelligence

          </button>

          <button className="nav-item" onClick={() => handleCategory("Technology")}>

            <Cpu size={18} /> Technology

          </button>

          <button className="nav-item" onClick={() => handleCategory("Business")}>

            <TrendingUp size={18} /> Business

          </button>

          <button className="nav-item">

            <Globe2 size={18} /> Other News

          </button>

        </nav>



        <div className="sidebar-label second-label">AI INFRASTRUCTURE</div>



        <div className="system-card">

          <div className="system-heading">

            <span className="live-dot" />

            <span>LOCAL AI ENGINE</span>

            <span className="online-text">ONLINE</span>

          </div>

          <div className="engine-icon">

            <BrainCircuit size={28} />

            <div className="engine-pulse" />

          </div>

          <h3>Llama 3.2</h3>

          <p>Local inference engine</p>

          <div className="system-footer">

            <span><Zap size={12} /> Ollama</span>

            <span>ACTIVE</span>

          </div>

        </div>



        <div className="sidebar-bottom">

          <div className="sidebar-profile">

            <div className="profile-avatar">N</div>

            <div>

              <strong>NewsGen AI</strong>

              <small>Mounesh workspace</small>

            </div>

          </div>

          <div className="sidebar-version">VERSION 1.0.0 · LOCAL EDITION</div>

        </div>

      </aside>



      {sidebarOpen && (

        <div className="mobile-overlay" onClick={() => setSidebarOpen(false)} />

      )}



      {/* MAIN AREA */}

      <main className="main-area">



        {/* TOP BAR */}

        <header className="topbar">

          <button className="mobile-menu" onClick={() => setSidebarOpen(true)}>

            <Menu size={21} />

          </button>



          <div className="breadcrumb">

            <span>Workspace</span>

            <ChevronRight size={14} />

            <strong>Intelligence Center</strong>

          </div>



          <div className="topbar-actions">

            <div className="system-status">

              <span className="live-dot" />

              NewS Update

            </div>

            <button className="icon-button" onClick={refreshDashboard} title="Refresh data">

              <RefreshCw size={17} className={refreshing ? "spin" : ""} />

            </button>

            <button className="icon-button" title="Notifications">

              <Bell size={17} />

            </button>

            <div className="top-avatar">VM</div>

          </div>

        </header>



        <div className="content">



          {/* HERO */}

          <section className="hero-section">

            <div className="hero-copy">

              <div className="eyebrow">

                <Sparkles size={14} />

                YOUR PERSONAL AI NEWS INTELLIGENCE

              </div>



              <h1>

                The world moves.

                <br />

                <span>We decode it.</span>

              </h1>



              <p>

                One intelligence layer for everything happening around you.

                Discover the stories, understand the signals, see the bigger picture.

              </p>



              <div className="hero-tags">

                <span><Radio size={13} /> LIVE NEWS STREAMS</span>

                <span><BrainCircuit size={13} /> AI-POWERED INSIGHTS</span>

              </div>

            </div>



            <div className="neural-visual">

              <div className="orbit orbit-outer" />

              <div className="orbit orbit-middle" />

              <div className="orbit orbit-inner" />

              <div className="neural-core">

                <BrainCircuit size={48} />

              </div>

              <div className="orbit-node node-one" />

              <div className="orbit-node node-two" />

              <div className="orbit-node node-three" />

              <div className="orbit-node node-four" />

              <div className="neural-caption">

                <span className="live-dot" />

                NEURAL ENGINE ACTIVE

              </div>

            </div>



            <div className="hero-watermark">NG / 01</div>

          </section>



          {/* STATS */}

          <section className="stats-section">

            <div className="section-heading">

              <div>

                <span className="section-kicker">SYSTEM OVERVIEW</span>

                <h2>Intelligence at a glance</h2>

              </div>

              <span className="updated-label">

                <span className="live-dot" /> DATABASE CONNECTED

              </span>

            </div>



            <div className="stats-grid">

              {statCards.map((stat, index) => {

                const Icon = stat.icon;

                return (

                  <div className={`stat-card stat-${stat.color}`} key={stat.label}>

                    <div className="stat-top">

                      <span>{stat.label}</span>

                      <div className="stat-icon"><Icon size={19} /></div>

                    </div>

                    <div className="stat-value">{stat.value}</div>

                    <div className="stat-bottom">

                      <span>{stat.detail}</span>

                      <ArrowUpRight size={15} />

                    </div>

                    <div className="stat-glow" />

                  </div>

                );

              })}

            </div>

          </section>



          {/* PROCESSING PIPELINE */}

          <section className="pipeline-panel">

            <div className="panel-heading">

              <div>

                <span className="section-kicker">BEHIND THE INTELLIGENCE</span>

                <h2>Neural processing architecture</h2>

              </div>

              <span className="pipeline-badge"><span className="live-dot" /> OPERATIONAL</span>

            </div>



            <div className="pipeline-flow">

              <div className="pipeline-step">

                <div className="pipeline-icon purple-icon"><Radio size={23} /></div>

                <div>

                  <strong>Ingestion</strong>

                  <small>RSS data streams</small>

                </div>

              </div>

              <div className="pipeline-connector"><span /></div>

              <div className="pipeline-step">

                <div className="pipeline-icon cyan-icon"><BrainCircuit size={23} /></div>

                <div>

                  <strong>Intelligence</strong>

                  <small>Llama 3.2 inference</small>

                </div>

              </div>

              <div className="pipeline-connector"><span /></div>

              <div className="pipeline-step">

                <div className="pipeline-icon green-icon"><Database size={23} /></div>

                <div>

                  <strong>Knowledge store</strong>

                  <small>SQLite database</small>

                </div>

              </div>

            </div>

          </section>



          {/* NEWS FEED */}

          <section className="news-section">

            <div className="section-heading news-heading">

              <div>

                <span className="section-kicker">DISCOVER WHAT MATTERS</span>

                <h2>Intelligence feed <span className="feed-count">{totalResults}</span></h2>

              </div>

              <div className="feed-live"><span className="live-dot" /> LIVE DATABASE</div>

            </div>



            <form className="search-bar" onSubmit={handleSearch}>

              <Search size={19} />

              <input

                value={keyword}

                onChange={(e) => setKeyword(e.target.value)}

                placeholder="Search stories, AI headlines, topics..."

              />

              {keyword && (

                <button type="button" className="clear-search" onClick={() => {

                  setKeyword("");

                  setSearch("");

                  setCategory("All");

                  setPage(1);

                }}>

                  <X size={16} />

                </button>

              )}

              <button type="submit" className="search-submit">

                SEARCH <Command size={13} />

              </button>

            </form>



            <div className="category-tabs">

              <button

                className={category === "All" ? "category-tab selected" : "category-tab"}

                onClick={() => handleCategory("All")}

              >

                All stories

              </button>

              {categories.map((item) => (

                <button

                  key={item}

                  className={category === item ? "category-tab selected" : "category-tab"}

                  onClick={() => handleCategory(item)}

                >

                  {item}

                </button>

              ))}

            </div>



            {error && <div className="error-message">{error}</div>}



            {loading && articles.length === 0 && !hasLoadedArticles ? (

              <div className="loading-panel">

                <div className="loading-orbit"><BrainCircuit size={30} /></div>

                <strong>Decoding intelligence...</strong>

                <span>Retrieving your news streams</span>

              </div>

            ) : articles.length === 0 ? (

              <div className="empty-panel">

                <Newspaper size={32} />

                <h3>No stories found</h3>

                <p>Try a different keyword or category.</p>

              </div>

            ) : (

              <div className="news-grid">

                {articles.map((article, index) => (

                  <article className="news-card" key={article.id}>

                    <div className="news-card-top">

                      <span className="news-index">STORY / {String(article.id).padStart(3, "0")}</span>

                      <span className="news-category">

                        {article.category || "GENERAL"}

                      </span>

                    </div>



                    <div className="news-source">

                      <Globe2 size={13} />

                      {article.source || "News source"}

                      <span>·</span>

                      {formatDate(article.published)}

                    </div>



                    <h3>{article.headline || article.title}</h3>



                    <p className="news-description">

                      {article.summary_text

                        ? article.summary_text

                            .replace(/\n/g, " ")

                            .replace(/\s+/g, " ")

                            .slice(0, 350)

                        : article.description}

                      {article.summary_text?.length > 350 ? "..." : ""}

                    </p>



                    <div className="news-card-footer">

                        <button

                            type="button"

                             className="read-briefing-button"

                              onClick={() => setSelectedArticle(article)}

                                   >

                        <Sparkles size={14} />

                       EXPLORE AI BRIEFING

                       <ArrowUpRight size={14} />

                       </button>



                      <span><Sparkles size={13} /> AI ANALYZED</span>

                      {article.url && (

                        <a href={article.url} target="\_blank" rel="noopener noreferrer">

                          READ SOURCE <ArrowUpRight size={14} />

                        </a>

                      )}

                    </div>

                    <div className={`news-card-accent accent-${index % 3}`} />

                  </article>

                ))}

              </div>

            )}





            {articles.length > 0 && !search && category === "All" && (

              <div className="pagination">

                <span>PAGE <strong>{page}</strong> OF {totalPages}</span>

                <div>

                  <button disabled={page <= 1} onClick={() => setPage(p => p - 1)}>

                    <ChevronLeft size={17} />

                  </button>

                  <button disabled={page >= totalPages} onClick={() => setPage(p => p + 1)}>

                    <ChevronRight size={17} />

                  </button>

                </div>

              </div>

            )}

          </section>



          {/* FOOTER */}

          <footer className="app-footer">

            <div><span className="footer-mark">NG</span> NEWSGEN AI <span>INTELLIGENCE PLATFORM</span></div>

            <div>POWERED BY OLLAMA <span>·</span> LLAMA 3.2 <span>·</span> LOCAL AI</div>

          </footer>

        </div>

      </main>

      <ArticleReader

  article={selectedArticle}

  onClose={() => setSelectedArticle(null)}

   />

    </div>

  );



  

}



export default App;
