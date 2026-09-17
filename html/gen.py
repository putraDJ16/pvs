#!/usr/bin/env python3
"""Generator halaman HTML statis PV Solution dari struktur Figma.
Output: file .html biasa (tanpa dependensi build). Jalankan ulang jika
partial sidebar/topbar diubah agar semua halaman tetap konsisten."""
import os, pathlib

OUT = pathlib.Path(__file__).parent

# --------------------------------------------------------------- ikon
S = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
 "star":    ('fill="currentColor"', '<path d="M12 2.5l2.7 6.02 6.55.63-4.93 4.37 1.42 6.43L12 16.6l-5.74 3.35 1.42-6.43L2.75 9.15l6.55-.63L12 2.5z"/>'),
 "home":    (S, '<path d="M3 9.5 12 3l9 6.5V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/><path d="M9 21v-7h6v7"/>'),
 "grid":    (S, '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>'),
 "filePlus":(S, '<path d="M14 3v5h5"/><path d="M19 8v11a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7z"/><path d="M12 12v5M9.5 14.5h5"/>'),
 "fileText":(S, '<path d="M14 3v5h5"/><path d="M19 8v11a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7z"/><path d="M9 13h6M9 17h4"/>'),
 "history": (S, '<path d="M8 3h8a1 1 0 0 1 1 1v1H7V4a1 1 0 0 1 1-1z"/><path d="M7 5H6a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1"/><path d="M8 11h8M8 15h5"/>'),
 "refresh": (S, '<path d="M21 12a9 9 0 1 1-2.6-6.4"/><path d="M21 3v6h-6"/>'),
 "list":    (S, '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>'),
 "alert":   (S, '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>'),
 "sync":    (S, '<path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/><path d="M3 21v-5h5"/>'),
 "logout":  (S, '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5"/><path d="M21 12H9"/>'),
 "plus":    (S, '<path d="M12 5v14M5 12h14"/>'),
 "search":  (S, '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>'),
 "check":   (S, '<path d="M20 6 9 17l-5-5"/>'),
 "x":       (S, '<path d="M18 6 6 18M6 6l12 12"/>'),
 "clock":   (S, '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>'),
 "checkCircle": (S, '<circle cx="12" cy="12" r="9"/><path d="m8.5 12.5 2.5 2.5 4.5-5"/>'),
 "upload":  (S, '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 9 5-5 5 5"/><path d="M12 4v12"/>'),
 "info":    (S, '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 7.5h.01"/>'),
}

def icon(name, size=20):
    attrs, body = ICONS[name]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" {attrs} '
            f'aria-hidden="true">{body}</svg>')

# ------------------------------------------------------------ partial
NAV = {
 "customer": [
   ("home",    "Home",                      "home",     "dashboard.html"),
   ("apply",   "Installation Application",   "filePlus", "application.html"),
   ("history", "Application History",        "history",  "history.html"),
 ],
 "pae": [
   ("dash",     "Dashboard",                  "grid",     "dashboard.html"),
   ("apply",    "Installation Application",   "filePlus", "application.html"),
   ("history",  "Application History",        "history",  "history.html"),
   ("update",   "Update Application Status",  "refresh",  "update-status.html"),
   ("activity", "Activity History",           "list",     "activity.html"),
 ],
}
USER = {
 "customer": ("Budi Santoso", "Customer", "B"),
 "pae":      ("Rina Wulandari", "PAE / Sales", "R"),
}

def head(title, depth):
    up = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · PV Solution</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/styles.css">
</head>
<body>"""

def sidebar(role, active):
    items = []
    for key, label, ic, href in NAV[role]:
        cls = "nav__item is-active" if key == active else "nav__item"
        items.append(f'      <a class="{cls}" href="{href}">{icon(ic)}<span>{label}</span></a>')
    nav = "\n".join(items)
    return f"""
  <aside class="sidebar">
    <div class="sidebar__brand">
      <span class="brandmark">{icon("star")}</span>
      <div>
        <div class="sidebar__name">PV Solution</div>
        <div class="sidebar__tag">Solar Energy Platform</div>
      </div>
    </div>

    <nav class="nav">
{nav}
    </nav>

    <div class="sidebar__foot">
      <a class="nav__item" href="../login.html">{icon("logout")}<span>Logout</span></a>
    </div>
  </aside>"""

def topbar(role, title, sub):
    name, roletxt, initial = USER[role]
    return f"""
    <header class="topbar">
      <div>
        <h1 class="h1">{title}</h1>
        <p class="topbar__sub">{sub}</p>
      </div>
      <div class="user">
        <div class="user__meta">
          <div class="user__name">{name}</div>
          <div class="user__role">{roletxt}</div>
        </div>
        <span class="avatar">{initial}</span>
      </div>
    </header>"""

def page(path, title, role, active, topbar_title, topbar_sub, content, modals="", depth=1):
    html = (head(title, depth) + '\n\n<div class="app">' + sidebar(role, active) +
            '\n\n  <div class="main">' + topbar(role, topbar_title, topbar_sub) +
            '\n\n    <main class="content">\n' + content + '\n    </main>\n  </div>\n</div>\n' +
            modals + f'\n<script src="{"../"*depth}assets/app.js"></script>\n</body>\n</html>\n')
    f = OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(html, encoding="utf-8")
    print("wrote", path)

# ----------------------------------------------------------- fragmen
BADGE = {
 "Submitted": "submitted", "Verification": "verification", "Survey": "survey",
 "Quotation": "quotation", "In Progress": "progress", "Completed": "completed",
}
def badge(status):
    return f'<span class="badge badge--{BADGE[status]}">{status}</span>'

def table(cols, rows, sm=False):
    cls = "data data--sm" if sm else "data"
    th = "".join(f"<th>{c}</th>" for c in cols)
    body = []
    for r in rows:
        body.append("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    return (f'      <div class="table-wrap">\n        <table class="{cls}">\n'
            f'          <thead><tr>{th}</tr></thead>\n          <tbody>\n            '
            + "\n            ".join(body) + '\n          </tbody>\n        </table>\n      </div>')

def stepper(steps, done):
    out = []
    for i, label in enumerate(steps, 1):
        cls = "step"
        if i <= done:
            cls += " is-done"
            if i < done:
                cls += " is-linked"
            else:
                cls += " is-current"
        dot = icon("check", 14) if i <= done else str(i)
        out.append(f'          <div class="{cls}"><span class="step__dot">{dot}</span>'
                   f'<span class="step__label">{label}</span></div>')
    return '        <div class="stepper">\n' + "\n".join(out) + "\n        </div>"

def kv(k, v):
    return f'<div><div class="detail__k">{k}</div><div class="detail__v">{v}</div></div>'

def select(label, placeholder, options, required=True, name=None):
    req = ' <span class="req">*</span>' if required else ""
    nm = name or label.lower().replace(" ", "-").replace("/", "")
    opts = "".join(f'<option>{o}</option>' for o in options)
    return (f'<div class="field"><label class="field__label" for="{nm}">{label}{req}</label>'
            f'<select class="select" id="{nm}" name="{nm}">'
            f'<option value="" selected>{placeholder}</option>{opts}</select></div>')

def text_field(label, placeholder, required=True, value=None, name=None, kind="text"):
    req = ' <span class="req">*</span>' if required else ""
    nm = name or label.lower().replace(" ", "-").replace("/", "")
    val = f' value="{value}"' if value else ""
    return (f'<div class="field"><label class="field__label" for="{nm}">{label}{req}</label>'
            f'<input class="input" type="{kind}" id="{nm}" name="{nm}" placeholder="{placeholder}"{val}></div>')

LOOKUP_CUSTOMER = f"""        <div class="lookup">
          <div class="lookup__title">PLN Customer ID Lookup (Optional)</div>
          <div class="lookup__row">
            <input class="input" type="text" placeholder="Enter PLN Customer ID" aria-label="PLN Customer ID">
            <button class="btn btn--primary" type="button">Check ID</button>
          </div>
        </div>"""

LOOKUP_PAE = LOOKUP_CUSTOMER.replace("Enter PLN Customer ID\"",
                                     "Enter PLN Customer ID (try: 5219038201)\"")

def application_form(role):
    lookup = LOOKUP_CUSTOMER if role == "customer" else LOOKUP_PAE
    if role == "customer":
        name_v, phone_v, email_v = "Budi Santoso", "0812-3456-7890", "budi@email.com"
        phone_ph, email_ph = "0812-3456-7890", "budi@email.com"
    else:
        name_v = phone_v = email_v = None
        phone_ph, email_ph = "0812-xxxx-xxxx", "customer@email.com"
    return f"""      <form class="form-stack" action="history.html">
{lookup}

        <div class="form-card">
          <h2 class="section-title">Customer Information</h2>
          <div class="form-grid">
            {text_field("Full Name", "Enter full name", True, name_v, "fullname")}
            {text_field("PLN Customer ID", "Optional", False, None, "pln-id")}
            {text_field("Phone Number", phone_ph, True, phone_v, "phone", "tel")}
            {text_field("Email", email_ph, True, email_v, "email", "email")}
            {select("Electricity User Type", "Select type...", ["Rumah Tangga (R1)", "Rumah Tangga (R2)", "Bisnis (B1)", "Industri (I1)"], True, "user-type")}
            {select("Current Power Capacity", "Select capacity...", ["900 VA", "1300 VA", "2200 VA", "3500 VA", "&gt; 3500 VA"], True, "current-capacity")}
          </div>
        </div>

        <div class="form-card">
          <h2 class="section-title">Installation Location</h2>
          <div class="form-grid">
            {select("Province", "Select province...", ["DKI Jakarta", "Jawa Barat", "Jawa Tengah", "Jawa Timur", "Banten"], True, "province")}
            {text_field("City / Regency", "e.g. Jakarta Selatan", True, None, "city")}
            {text_field("District", "e.g. Mampang Prapatan", True, None, "district")}
            {text_field("Subdistrict", "e.g. Mampang", True, None, "subdistrict")}
            <div class="field span-2">
              <label class="field__label" for="address">Full Address <span class="req">*</span></label>
              <textarea class="textarea" id="address" name="address" placeholder="Enter complete installation address"></textarea>
            </div>
            {select("Planned Solar Capacity", "Select capacity...", ["1 kWp", "2 kWp", "3 kWp", "4 kWp", "5 kWp"], True, "planned-capacity")}
          </div>
        </div>

        <div class="form-actions">
          <a class="btn btn--ghost" href="dashboard.html">Cancel</a>
          <button class="btn btn--primary" type="submit">Submit Application</button>
        </div>
      </form>"""

# =================================================== HALAMAN CUSTOMER
page("customer/dashboard.html", "Home", "customer", "home", "Home", "Welcome to PV Solution", f"""      <section class="hero">
        <div>
          <h2 class="h2">Welcome back, Budi!</h2>
          <p class="hero__sub">You have <strong>2</strong> active applications in progress.</p>
        </div>
        <a class="btn btn--accent" href="application.html">{icon("plus",16)}Apply for Installation</a>
      </section>

      <section class="stats">
        <div class="stat"><span class="stat__icon tone-blue"><span class="stat-num">2</span></span><span class="stat__label">Total Applications</span></div>
        <div class="stat"><span class="stat__icon tone-orange"><span class="stat-num">2</span></span><span class="stat__label">In Progress</span></div>
        <div class="stat"><span class="stat__icon tone-green"><span class="stat-num">0</span></span><span class="stat__label">Completed</span></div>
      </section>

      <section class="card">
        <div class="card__head">
          <h2 class="h3">Recent Applications</h2>
          <a class="link-btn" href="history.html">View all</a>
        </div>
{table(["Application No.","Date","Location","Capacity","Status","Action"], [
  ['<span class="ref">PVS-2024-0001</span>','2024-01-15','Jakarta Selatan, DKI Jakarta','3 kWp',badge("Survey"),'<a class="link-btn" href="history.html">View Detail</a>'],
  ['<span class="ref">PVS-2024-0004</span>','2024-02-15','Jakarta Selatan, DKI Jakarta','4 kWp',badge("Verification"),'<a class="link-btn" href="history.html">View Detail</a>'],
])}
      </section>""")

page("customer/application.html", "Installation Application", "customer", "apply",
     "Installation Application", "Submit a new solar panel installation request",
     application_form("customer"))

CUST_DETAIL_MODAL = f"""
<div class="modal-overlay" id="detail-modal">
  <div class="modal modal--wide">
    <div class="modal__head">
      <h2 class="h3">Application Detail — PVS-2024-0001</h2>
      <button class="modal__close" type="button" data-modal-close aria-label="Close">{icon("x")}</button>
    </div>
    <div class="modal__body">
      <div>
        <div class="modal-section__title">Application Progress</div>
{stepper(["Submitted","Verification","Survey","Quotation","In Progress","Completed"], 3)}
      </div>

      <div class="modal-section">
        <div class="detail-grid">
          {kv("Application Number","PVS-2024-0001")}
          {kv("Application Date","2024-01-15")}
          {kv("PLN Customer ID","5219038201")}
          {kv("Electricity Type","Rumah Tangga (R2)")}
          {kv("Current Capacity","2200 VA")}
          {kv("Planned Capacity","3 kWp")}
        </div>
      </div>

      <div class="modal-section">
        <div class="modal-section__title">Installation Location</div>
        <div class="detail-grid" style="margin-top:12px">
          {kv("Province","DKI Jakarta")}
          {kv("City / Regency","Jakarta Selatan")}
          {kv("District","Mampang Prapatan")}
          {kv("Subdistrict","Mampang")}
          <div style="grid-column:1/-1">{kv("Full Address","Jl. Mampang Indah No. 45")[5:-6]}</div>
        </div>
      </div>

      <div class="modal-section">
        <div class="modal-section__title">Notes</div>
        <div class="panel" style="margin-top:8px;padding:12px 16px">
          <p class="label-700" style="font-weight:400">Survei dijadwalkan 22 Januari 2024</p>
        </div>
      </div>
    </div>
  </div>
</div>"""

HIST_FILTERS = f"""      <section class="card filterbar">
        <div class="filters">
          <div class="search">{icon("search",16)}<input class="input" type="search" placeholder="Search by application no. or address..." aria-label="Search"></div>
          <select class="select" aria-label="Status"><option>All Statuses</option><option>Submitted</option><option>Verification</option><option>Survey</option><option>Quotation</option><option>In Progress</option><option>Completed</option></select>
          <input class="input input--date" type="month" aria-label="Month">
          <button class="btn btn--ghost" type="button">Reset Filter</button>
        </div>
      </section>"""

page("customer/history.html", "Application History", "customer", "history",
     "Application History", "Track all your installation applications", f"""{HIST_FILTERS}

      <section class="card">
        <div class="card__head">
          <h2 class="h3">Applications</h2>
          <span class="count">2 records</span>
        </div>
{table(["Application No.","Date","Location","Capacity","Status","Action"], [
  ['<span class="ref">PVS-2024-0001</span>','2024-01-15','Jakarta Selatan, DKI Jakarta','3 kWp',badge("Survey"),'<button class="link-btn" type="button" data-modal-open="detail-modal">View Detail</button>'],
  ['<span class="ref">PVS-2024-0004</span>','2024-02-15','Jakarta Selatan, DKI Jakarta','4 kWp',badge("Verification"),'<button class="link-btn" type="button" data-modal-open="detail-modal">View Detail</button>'],
])}
      </section>""", modals=CUST_DETAIL_MODAL)

# ======================================================== HALAMAN PAE
PAE_ROWS = [
  ("PVS-2024-0001","Budi Santoso","2024-01-15","Jakarta Selatan, DKI Jakarta","Survey"),
  ("PVS-2024-0002","Sari Dewi","2024-01-22","Bandung, Jawa Barat","Quotation"),
  ("PVS-2024-0003","Ahmad Fauzi","2024-02-05","Tangerang, Banten","Submitted"),
  ("PVS-2023-0045","Dewi Rahayu","2023-11-10","Jakarta Barat, DKI Jakarta","Completed"),
  ("PVS-2024-0004","Budi Santoso","2024-02-15","Jakarta Selatan, DKI Jakarta","Verification"),
]

SYNC_MODAL = f"""
<div class="modal-overlay" id="sync-modal">
  <div class="modal modal--slim">
    <div class="modal__head">
      <h2 class="h3">Sync Data to P4B</h2>
      <button class="modal__close" type="button" data-modal-close aria-label="Close">{icon("x")}</button>
    </div>
    <div class="modal__body modal__body--plain">

      <!-- State "konfirmasi" — di Figma layer ini di-hide. Hapus [hidden] untuk melihatnya. -->
      <div class="note" hidden>
        {icon("info",20)}
        <div>
          <p class="strong" style="color:var(--brand-900);font-size:14px;line-height:20px">Sync to P4B Application</p>
          <p style="margin-top:2px;color:var(--brand-500)">This will transmit 5 application records from PV Solution to the P4B system. Existing P4B records will be updated if the application number matches.</p>
        </div>
      </div>

      <!-- State "selesai" — yang tampil di Figma -->
      <div class="result-state">
        <div class="result-state__icon">{icon("check",28)}</div>
        <h3 class="h3 result-state__title">Sync Completed Successfully</h3>
        <p class="result-state__sub">All application data has been transmitted to P4B.</p>

        <div class="result-stats" hidden>
          <div style="background:var(--green-bg);border:1px solid var(--green-bd)">
            <div class="n" style="color:var(--green-fg)">5</div><div class="k" style="color:#00A63E">Records Sent</div>
          </div>
          <div style="background:var(--gray-50);border:1px solid var(--gray-200)">
            <div class="n" style="color:var(--gray-400)">0</div><div class="k" style="color:var(--gray-400)">Failed</div>
          </div>
        </div>

        <p class="result-state__meta">Synced at 10 Sep 2026, 09.34</p>
      </div>

      <div class="form-actions" style="padding-top:20px;margin-top:4px;border-top:1px solid var(--gray-100)">
        <button class="btn" style="background:#00A63E;color:#fff" type="button" data-modal-close>Done</button>
      </div>
    </div>
  </div>
</div>"""

page("pae/dashboard.html", "Dashboard", "pae", "dash", "Dashboard", "PAE / Sales Overview", f"""      <section class="row--between">
        <div>
          <h2 class="h3" style="color:var(--gray-800)">Good morning, Rina</h2>
          <p class="muted">February 2024 — Here's your sales summary</p>
        </div>
        <div class="row gap-8">
          <button class="btn btn--ghost" type="button" data-modal-open="sync-modal">{icon("sync",16)}Sync Data to P4B</button>
          <a class="btn btn--primary" href="application.html">{icon("plus",16)}New Application</a>
        </div>
      </section>

      <section class="stats">
        <div class="kpi">
          <div class="kpi__top"><span class="kpi__label">Applications Submitted</span><span class="kpi__icon fill-brand">{icon("fileText")}</span></div>
          <div class="kpi__num num-brand">5</div>
        </div>
        <div class="kpi">
          <div class="kpi__top"><span class="kpi__label">Follow Up Required</span><span class="kpi__icon fill-orange">{icon("alert")}</span></div>
          <div class="kpi__num num-orange">3</div>
        </div>
        <div class="kpi">
          <div class="kpi__top"><span class="kpi__label">Monthly Closing</span><span class="kpi__icon fill-green">{icon("checkCircle")}</span></div>
          <div class="kpi__num num-green">0</div>
        </div>
      </section>

      <section class="dash-2col">
        <div class="card">
          <div class="card__head">
            <h2 class="h3">Recent Applications</h2>
            <a class="link-btn" href="history.html">View all</a>
          </div>
{table(["App No.","Customer","Date","Location","Status"], [
  [f'<span class="ref">{no}</span>', cust, date, loc.split(",")[0], badge(st)]
  for no,cust,date,loc,st in PAE_ROWS
], sm=True)}
        </div>

        <div class="card">
          <div class="card__head" style="display:block">
            <h2 class="h3">Today's Schedule</h2>
            <p class="small" style="padding-top:2px;color:var(--gray-400)">10 September 2026</p>
          </div>
          <div>
            <div class="schedule__row">
              <div class="schedule__time">09:00</div>
              <div class="grow">
                <div class="schedule__who">Budi Santoso</div>
                <div class="schedule__what">Site Survey</div>
                <div class="schedule__tag"><span class="badge badge--submitted">Survey Scheduled</span></div>
              </div>
            </div>
            <div class="schedule__row">
              <div class="schedule__time">11:30</div>
              <div class="grow">
                <div class="schedule__who">Sari Dewi</div>
                <div class="schedule__what">Quotation Presentation</div>
                <div class="schedule__tag"><span class="badge badge--submitted">Note Added</span></div>
              </div>
            </div>
            <div class="schedule__row">
              <div class="schedule__time">14:00</div>
              <div class="grow">
                <div class="schedule__who">Ahmad Fauzi</div>
                <div class="schedule__what">Follow-up Call</div>
                <div class="schedule__tag"><span class="badge badge--submitted">Status Updated</span></div>
              </div>
            </div>
          </div>
        </div>
      </section>""", modals=SYNC_MODAL)

page("pae/application.html", "Installation Application", "pae", "apply",
     "Installation Application", "Create application on behalf of a customer",
     application_form("pae"))

PAE_FILTERS = HIST_FILTERS.replace("application no. or address...", "application no. or customer name...")

PAE_DETAIL_MODAL = f"""
<div class="modal-overlay" id="detail-modal">
  <div class="modal modal--wide">
    <div class="modal__head">
      <h2 class="h3">Application — PVS-2024-0001</h2>
      <button class="modal__close" type="button" data-modal-close aria-label="Close">{icon("x")}</button>
    </div>
    <div class="modal__body">
      <div>
        <div class="modal-section__title">Progress</div>
{stepper(["Submitted","Verification","Survey","Quotation","In Progress","Completed"], 3)}
      </div>

      <div class="modal-section">
        <div class="detail-grid">
          {kv("Application Number","PVS-2024-0001")}
          {kv("Customer Name","Budi Santoso")}
          {kv("Phone Number","0812-3456-7890")}
          {kv("PLN Customer ID","5219038201")}
          {kv("Application Date","2024-01-15")}
          {kv("Planned Capacity","3 kWp")}
          {kv("Current Capacity","2200 VA")}
          {kv("Electricity Type","Rumah Tangga (R2)")}
        </div>
      </div>

      <div class="modal-section">
        <div class="modal-section__title">Location</div>
        <p class="label-700" style="margin-top:12px;font-weight:400">Jl. Mampang Indah No. 45, Mampang, Mampang Prapatan, Jakarta Selatan, DKI Jakarta</p>
      </div>

      <div class="modal-section">
        <div class="modal-section__title">Notes</div>
        <div class="panel" style="margin-top:8px;padding:12px 16px">
          <p class="label-700" style="font-weight:400">Survei dijadwalkan 22 Januari 2024</p>
        </div>
      </div>
    </div>
  </div>
</div>"""

page("pae/history.html", "Application History", "pae", "history",
     "Application History", "All customer installation applications", f"""{PAE_FILTERS}

      <section class="card">
        <div class="card__head">
          <h2 class="h3">Applications</h2>
          <span class="count">5 records</span>
        </div>
{table(["Application No.","Customer","Date","Location","Status","Action"], [
  [f'<span class="ref">{no}</span>', cust, date, loc, badge(st),
   '<button class="link-btn" type="button" data-modal-open="detail-modal">View Detail</button>']
  for no,cust,date,loc,st in PAE_ROWS
])}
      </section>""", modals=PAE_DETAIL_MODAL)

UPDATE_MODAL = f"""
<div class="modal-overlay" id="update-modal">
  <div class="modal modal--mid">
    <div class="modal__head">
      <h2 class="h3">Update Application Status</h2>
      <button class="modal__close" type="button" data-modal-close aria-label="Close">{icon("x")}</button>
    </div>
    <div class="modal__body">
      <div class="summary-panel">
        <div><div class="detail__k">Application No.</div><div class="detail__v strong">PVS-2024-0001</div></div>
        <div><div class="detail__k">Customer</div><div class="detail__v strong">Budi Santoso</div></div>
        <div><div class="detail__k">Location</div><div class="label-700" style="font-weight:400">Jakarta Selatan, DKI Jakarta</div></div>
        <div><div class="detail__k">Current Status</div><div style="margin-top:4px">{badge("Survey")}</div></div>
      </div>

      <div class="field">
        <label class="field__label" for="new-status">New Status <span class="req">*</span></label>
        <select class="select" id="new-status" name="new-status">
          <option value="" selected>Select new status...</option>
          <option>Verification</option><option>Survey</option><option>Quotation</option>
          <option>In Progress</option><option>Completed</option>
        </select>
      </div>

      <div class="field">
        <label class="field__label" for="followup">Follow-up Date</label>
        <input class="input" type="date" id="followup" name="followup">
      </div>

      <div class="field">
        <label class="field__label" for="notes">Notes</label>
        <textarea class="textarea" id="notes" name="notes" style="min-height:84px" placeholder="Enter any notes about this status update..."></textarea>
      </div>

      <div class="note" style="display:block"><strong>Note:</strong> Saving this change will automatically create an activity record in Activity History.</div>
    </div>
    <div class="modal__foot">
      <button class="btn btn--ghost" type="button" data-modal-close>Cancel</button>
      <button class="btn btn--primary" type="button" style="opacity:.5">Save Changes</button>
    </div>
  </div>
</div>"""

page("pae/update-status.html", "Update Application Status", "pae", "update",
     "Update Application Status", "Review and update the progress of customer applications", f"""{PAE_FILTERS}

      <section class="card">
        <div class="card__head">
          <h2 class="h3">Applications</h2>
          <span class="count">5 records</span>
        </div>
{table(["Application No.","Customer","Date","Location","Current Status","Action"], [
  [f'<span class="ref">{no}</span>', cust, date, loc, badge(st),
   '<button class="link-btn" type="button" data-modal-open="update-modal">Update</button>']
  for no,cust,date,loc,st in PAE_ROWS
])}
      </section>""", modals=UPDATE_MODAL)

ACT_BADGE = {"Status Updated": "submitted", "Survey Scheduled": "survey", "Note Added": "note"}

ACT_ROWS = [
 ("2024-01-15 09:30","System","PVS-2024-0001","Budi Santoso","Status Updated","Status changed to Submitted"),
 ("2024-01-16 14:15","Rina Wulandari","PVS-2024-0001","Budi Santoso","Status Updated","Status changed to Verification"),
 ("2024-01-18 10:00","Rina Wulandari","PVS-2024-0001","Budi Santoso","Survey Scheduled","Survey scheduled for 22 January 2024 at 09:00"),
 ("2024-01-22 11:45","Rina Wulandari","PVS-2024-0001","Budi Santoso","Status Updated","Status changed to Survey"),
 ("2024-01-22 09:30","System","PVS-2024-0002","Sari Dewi","Status Updated","Status changed to Submitted"),
 ("2024-01-23 16:00","Rina Wulandari","PVS-2024-0002","Sari Dewi","Note Added","Customer requested expedited processing"),
 ("2024-01-25 13:30","Rina Wulandari","PVS-2024-0002","Sari Dewi","Status Updated","Status changed to Quotation"),
 ("2024-02-05 09:00","System","PVS-2024-0003","Ahmad Fauzi","Status Updated","Status changed to Submitted"),
]

page("pae/activity.html", "Activity History", "pae", "activity",
     "Activity History", "Audit trail of all application activities", f"""      <section class="card filterbar">
        <div class="filters">
          <div class="search">{icon("search",16)}<input class="input" type="search" placeholder="Search by app no., customer, or activity..." aria-label="Search"></div>
          <select class="select" aria-label="Activity type"><option>All Activity Types</option><option>Status Updated</option><option>Survey Scheduled</option><option>Note Added</option></select>
          <select class="select" aria-label="User"><option>All Users</option><option>Rina Wulandari</option><option>System</option></select>
        </div>
        <div class="filters">
          <span class="filter-label">From</span><input class="input input--date" type="date" aria-label="From date">
          <span class="filter-label">To</span><input class="input input--date" type="date" aria-label="To date">
          <button class="btn btn--ghost" type="button">Reset Filter</button>
        </div>
      </section>

      <section class="card">
        <div class="card__head">
          <h2 class="h3">Activity Log</h2>
          <span class="count">11 records</span>
        </div>
{table(["Date &amp; Time","User","Application No.","Customer","Activity Type","Activity Detail"], [
  [f'<span class="nowrap">{dt}</span>', f'<span class="label-700">{u}</span>',
   f'<span class="ref">{no}</span>', cust,
   f'<span class="badge badge--{ACT_BADGE[typ]}">{typ}</span>', detail]
  for dt,u,no,cust,typ,detail in ACT_ROWS
])}
      </section>""")

# ============================================================== INDEX
LINKS = [
 ("Login Page", "Halaman masuk & registrasi", [
   ("login.html", "Login", "Sign in — panel brand + form"),
   ("register.html", "Register", "Create an Account"),
   ("register-invalid.html", "Register — validation", "Semua field menampilkan pesan error"),
 ]),
 ("Customer UI", "Tampilan untuk pelanggan (Budi Santoso)", [
   ("customer/dashboard.html", "Home", "Welcome banner, ringkasan, tabel terbaru"),
   ("customer/application.html", "Installation Application", "Form pengajuan instalasi"),
   ("customer/history.html", "Application History", "Daftar + modal detail (klik View Detail)"),
 ]),
 ("PAE UI", "Tampilan untuk PAE / Sales (Rina Wulandari)", [
   ("pae/dashboard.html", "Dashboard", "KPI, recent applications, today's schedule, modal Sync P4B"),
   ("pae/application.html", "Installation Application", "Form atas nama pelanggan"),
   ("pae/history.html", "Application History", "Daftar semua pengajuan + modal detail"),
   ("pae/update-status.html", "Update Application Status", "Daftar + modal update status"),
   ("pae/activity.html", "Activity History", "Audit trail aktivitas"),
 ]),
]

groups = []
for title, sub, items in LINKS:
    cards = "\n".join(
        f'        <a class="index-card" href="{href}"><div class="t">{name}</div><div class="d">{desc}</div></a>'
        for href, name, desc in items)
    groups.append(f"""    <section class="index-group">
      <h2 class="h2">{title}</h2>
      <p>{sub}</p>
      <div class="index-grid">
{cards}
      </div>
    </section>""")

index = (head("Screens", 0) + f"""

<div class="index-page">
  <header style="margin-bottom:40px">
    <div class="auth-logo" style="justify-content:flex-start">
      <span class="auth-logo__mark"><span>{icon("star",16)}</span></span>
      <span class="auth-logo__name">PV Solution</span>
    </div>
    <h1 class="display-sm" style="margin-top:20px">Screens</h1>
    <p class="muted" style="margin-top:4px">Hasil konversi Figma &ldquo;PV Solution&rdquo; ke HTML + CSS statis. 11 layar, 4 modal.</p>
  </header>

""" + "\n\n".join(groups) + """
</div>

</body>
</html>
""")
(OUT / "index.html").write_text(index, encoding="utf-8")
print("wrote index.html")

# ======================================================= REGISTER (2 state)
EYE = """<button class="input-group__btn" type="button" data-toggle-password aria-label="Show password">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle>
              </svg>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none" aria-hidden="true">
                <path d="M10.7 5.1A10.4 10.4 0 0 1 12 5c6.5 0 10 7 10 7a18 18 0 0 1-2.2 3.1M6.6 6.6A18 18 0 0 0 2 12s3.5 7 10 7a10.4 10.4 0 0 0 4.2-.9"></path><path d="m2 2 20 20"></path>
              </svg>
            </button>"""

def reg_field(label, fid, ph, kind, err, invalid, pw=False):
    cls = "field field--invalid" if invalid else "field"
    ctrl = (f'<div class="input-group"><input class="input" id="{fid}" name="{fid}" type="password" '
            f'placeholder="{ph}" autocomplete="new-password">{EYE}</div>') if pw else \
           (f'<input class="input" id="{fid}" name="{fid}" type="{kind}" placeholder="{ph}">')
    msg = f'\n            <p class="field__error">{err}</p>' if invalid else ""
    return (f'<div class="{cls}">\n            <label class="field__label" for="{fid}">{label}</label>\n'
            f'            {ctrl}{msg}\n          </div>')

def register_page(invalid):
    name = "register-invalid.html" if invalid else "register.html"
    title = "Create an Account (validation)" if invalid else "Create an Account"
    terms_err = ('\n            <p class="field__error" style="margin-top:4px">You must agree to the '
                 'terms and conditions.</p>') if invalid else ""
    html = head(title, 0) + f"""

<div class="auth-center">
  <div class="auth-center__inner">

    <div class="auth-logo">
      <span class="auth-logo__mark"><span>{icon("star",16)}</span></span>
      <span class="auth-logo__name">PV Solution</span>
    </div>

    <div class="auth-card">
      <h1 class="h2">Create an Account</h1>
      <p class="auth-card__sub">Register as a new PV Solution customer</p>

      <form action="login.html">
        <div class="col">
          {reg_field("Full Name","fullname","Enter your full name","text","Full name is required.",invalid)}
        </div>

        <div class="pair">
          {reg_field("Phone Number","phone","0812-xxxx-xxxx","tel","Phone number is required.",invalid)}
          {reg_field("Email","email","you@email.com","email","Email is required.",invalid)}
        </div>

        <div class="col">
          {reg_field("Password","password","Min. 8 characters","password","Password is required.",invalid,pw=True)}
        </div>

        <div class="col">
          {reg_field("Confirm Password","confirm","Re-enter password","password","Please confirm your password.",invalid,pw=True)}
        </div>

        <div>
          <div class="checkline">
            <input id="terms" name="terms" type="checkbox">
            <label class="muted-600" for="terms">I agree to the <a href="#">Terms and Conditions</a> and <a href="#">Privacy Policy</a></label>
          </div>{terms_err}
        </div>

        <button class="btn btn--primary btn--block" type="submit">Create Account</button>
      </form>

      <p class="auth-card__foot">Already have an account? <a href="login.html">Sign in</a></p>
    </div>

  </div>
</div>

<script src="assets/app.js"></script>
</body>
</html>
"""
    (OUT / name).write_text(html, encoding="utf-8")
    print("wrote", name)

register_page(False)
register_page(True)
