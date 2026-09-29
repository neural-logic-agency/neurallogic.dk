#!/usr/bin/env python3
"""Build the reading pages of neurallogic.dk, plus sitemap.xml.

Why they exist: an assistant answering "who builds AI colleagues that read a company's
archives in Europe" quotes passages, not whole sites. The front page is one scroll-driven
document; these pages give each buyer question its own address, heading and paragraph.

Every page here is plain HTML on the shared pages.css. Content lives in PAGES below, so
head, header, footer, the visitor counter and the sitemap can never drift apart.

    python3 build/pages.py        writes the pages and sitemap.xml

Nothing in here may claim more than the front page and llms.txt claim. Frida and Vera are
in preparation; Pia runs daily on a shop of our own. Keep it that way.
"""
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from content_conversion import CONVERSION_DA, CONVERSION_DE, CONVERSION_EN  # noqa: E402
from content_de import HOW_IT_WORKS_DE, LAW_DE, PROPERTY_DE, QUESTIONS_DE  # noqa: E402
from content_da import HOW_IT_WORKS_DA, LAW_DA, PROPERTY_DA, QUESTIONS_DA  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://neurallogic.dk"

# ---------------------------------------------------------------- content

HOW_IT_WORKS = [
    ("h2", "What you hand over"),
    ("p", "A copy. Not a migration, not a new system to move into, not a year of preparation. "
          "A daily copy of the archives you already keep: the data room, the mail archive, the "
          "accounting export, the shared drive, the scans nobody has opened since they were filed."),
    ("p", "Nothing is read before you have said so in writing, in a data-processing agreement "
          "with Axon Trade ApS, the Danish company behind Neural Logic. You say which archives "
          "are in scope, and that is the boundary."),
    ("h2", "Conversion: files become an addressable archive"),
    ("p", "Every document is read once, properly. A scan becomes text, a contract becomes clauses, "
          "a mail thread becomes dated messages, a protocol becomes decisions. Each piece keeps a "
          "link back to the page it came from, so any sentence can be traced to its original."),
    ("p", "The result is an archive you own: checked, addressable and usable with any language "
          "model, ours or the one you choose in three years. That is deliberate. A client who "
          "cannot leave is not a client, only a captive."),
    ("h2", "The register: what is there, and what is not"),
    ("p", "While the documents are read, a register is built: which contract carries which clause, "
          "which protocol is signed, which invoice belongs to which case, which document was expected "
          "and never arrived. The register is a record, not a memory."),
    ("p", "This is what makes “not found” a real answer. When the colleague says a termination "
          "clause is missing, that comes from the register, which knows every document it read and "
          "every place the clause could have been. It is not a model failing to recall something."),
    ("h2", "Reading a case"),
    ("p", "You ask about a case, a property, a client, a contract or a project. The colleague "
          "assembles the complete file in date order across every archive in scope, quotes the "
          "passages that decide the question word for word with a link to the original, and states "
          "plainly what it looked for and did not find."),
    ("p", "What comes back is a file, not a chat answer: the documents, the order they happened in, "
          "the decisive words, and the gaps. A person reads it and decides."),
    ("h2", "Every quotation is checked"),
    ("p", "Before a quotation reaches you it is compared, word for word, with the source document. "
          "If it does not match, it is held back and you are told. A colleague that quotes a "
          "contract almost correctly is worse than no colleague at all, because the mistake looks "
          "exactly like the truth."),
    ("h2", "Two roles, one boundary"),
    ("p", "The colleague who reads your documents runs on a European model, Mistral, processed in "
          "Europe under a European contract. Documents do not leave that boundary."),
    ("p", "Behind her stands a supervisor that never sees a document or a name. It reads only the "
          "shape of the work: what kind of question was asked, how many documents were read, which "
          "word was missing, where the reading went wrong. Because nothing of yours reaches it, it "
          "is chosen for thinking rather than for location: today that is Claude, from Anthropic, in "
          "our view the best model for this kind of task. It improves the colleague a little every "
          "night, without any access to your data."),
    ("h2", "What it is not"),
    ("ul", [
        "<b>Not a chatbot on your intranet.</b> It answers from a checked register built while "
        "reading your documents, not from a model's recollection of them.",
        "<b>Not a decision-maker.</b> It lays out facts. A person weighs them and acts.",
        "<b>Not a judge of people.</b> Files on buildings, products, contracts and cases. No scores, "
        "no rankings, no predictions about people.",
        "<b>Not a writer into your systems.</b> Writing back is off by default and switched on only "
        "by invitation, where you ask for it and the rules allow it.",
    ]),
    ("h2", "Where this stands today"),
    ("p", "Frida, the document colleague, is in preparation, with the first client engagement being "
          "prepared now. Vera, the supervisor, is in preparation. Pia, a catalogue colleague built "
          "on the same method, runs every day on a web shop of our own, reading a supplier's feed "
          "and keeping the shop true to it."),
]

QUESTIONS = [
    ("What does Neural Logic actually deliver?",
     ["An AI colleague that reads the archives your company already holds and, for any case you ask "
      "about, lays out the complete file in date order, quotes the passages that decide it word for "
      "word with a link to the original, and states what it looked for and did not find.",
      "Alongside it you get the archive itself: your files converted into a checked, addressable "
      "form that works with any language model, and a register of what each document contains."]),
    ("Does our data leave Europe?",
     ["No. The colleague that reads documents runs on a European model, Mistral, processed in Europe "
      "under a European contract, and the work happens under a data-processing agreement with Axon "
      "Trade ApS, a Danish company.",
      "The supervisor that improves the colleague overnight never sees a document or a name, so it is "
      "chosen for its abilities rather than its location: today that is Claude, from Anthropic, running "
      "outside Europe. It reads only the shape of the work — what was asked, how many documents, "
      "which word was missing — and never your material."]),
    ("Do we have to migrate our documents or change systems?",
     ["No. A daily copy of the archives you already keep is enough: a data room, a mail archive, an "
      "accounting export, a shared drive. Nothing has to be moved into a new system, and your people "
      "keep working exactly where they work now."]),
    ("What kinds of archives and files can it read?",
     ["Contracts, correspondence, invoices, protocols, reports and scans, across several archives at "
      "once. Scanned paper is read as text, so documents that were never searchable become part of "
      "the file like any other."]),
    ("What happens when the answer is not in the documents?",
     ["You are told. “Not found” is a first-class answer here, and it comes from the register built "
      "while every document was read, not from a model's memory. Whether a clause, a signature or a "
      "protocol is missing is a fact about your archive, and it is answered as one.",
      "For most of the work our clients care about, knowing that something is missing is worth as "
      "much as finding it."]),
    ("How do you stop it from inventing quotations?",
     ["Every quotation is compared word for word with its source document before it reaches the "
      "reader. If it does not match, it is held back and the reader is told. Nothing reaches you on "
      "the strength of sounding right."]),
    ("How is this different from asking ChatGPT or Copilot about our files?",
     ["A general assistant answers from what it retrieved and what it recalls, and it cannot tell you "
      "what it failed to find. This is the difference that matters in a file that carries money or "
      "liability.",
      "A document colleague reads every document in scope, keeps a register of what is in them, "
      "quotes only what it has verified against the source, and names the gaps. It also keeps the "
      "boundary: your documents stay inside a European contract."]),
    ("Who do we sign with, and who is liable?",
     ["Axon Trade ApS, a Danish private limited company in Copenhagen, register number CVR 45 92 07 63. "
      "Neural Logic is a brand of that company, not a separate legal entity. Contracts, invoices and "
      "the data-processing agreement all name Axon Trade ApS, and the company is signed for by its "
      "director."]),
    ("What does a first engagement look like?",
     ["Small and measured. A short first contract on a real case of yours rather than a demonstration, "
      "with acceptance judged on what it produces; then two further short phases. You can stop after "
      "any phase and keep everything built so far, including the converted archive, the register and "
      "the glossary.",
      "The point of starting this way is that you decide on evidence from your own files, not on "
      "slides. And the first phase is worth having even if you decide to stop there, for the reason "
      "in the next answer."]),
    ("If we stop after the first phase, what have we actually got?",
     ["The thing every company will need anyway: your files converted into a checked, machine-readable "
      "archive, with a register of what each document contains and a glossary of your own vocabulary. "
      "It is not built for our software. It works with any language model, ours or whichever one you "
      "choose in three years.",
      "Almost every company will have to do this work at some point. Documents that only exist as "
      "scans, PDFs and mail threads cannot be used by any AI worth trusting, and converting them is "
      "the slow part — not the clever part that comes after. Doing it on a small first contract, on "
      "real cases, with the result yours to keep, is a cheap way to have it behind you.",
      "That is why we treat the first phase as a commitment rather than a trial: whatever you decide "
      "about us afterwards, you are further along than you were."]),
    ("What does it cost?",
     ["It is priced per engagement, because the work depends on how much you hold and in what state. "
      "The first phase is deliberately small, so the first decision is a small one. Write to us with "
      "a rough idea of the archives involved and you get a straight answer."]),
    ("Which languages does the colleague work in?",
     ["Danish, German and English. The company is in Copenhagen and its founder is German, so the "
      "written work happens in all three without translation in between."]),
    ("Who is behind Neural Logic?",
     ["Thomas Möller, founder and sole owner of Axon Trade ApS in Copenhagen, which also operates "
      "the hockey shop Hockey24. The company facts, including the register extract, are on the "
      "<a href=\"https://axontrade.dk/\">Axon Trade page</a>."]),
]

PROPERTY = [
    ("h2", "The problem in this trade"),
    ("p", "A property carries decades of paper: the purchase, the leases and their amendments, the "
          "handover protocols, the defect lists, the correspondence with tenants and contractors, the "
          "insurance case nobody closed, the invoices that belong to a repair somebody remembers "
          "differently. It sits in a data room, a mail archive and a shared drive, and nobody has "
          "time to read all three."),
    ("p", "So the question “what exactly did we agree about this roof, and when” costs an afternoon, "
          "and is answered from memory more often than anyone admits."),
    ("h2", "What the colleague does with it"),
    ("ul", [
        "<b>The complete file for one object.</b> Everything about a property, a unit or a tenancy, "
        "in date order, across every archive in scope.",
        "<b>The clause that decides it, quoted.</b> Which lease version governs, what it says about "
        "the obligation in question, word for word, with a link to the page it came from.",
        "<b>What is missing, named.</b> The handover protocol that was never signed, the amendment "
        "referred to but absent, the certificate that expired. From the register, not from a guess.",
        "<b>The history of a dispute.</b> Every message, protocol and invoice that touches a case, "
        "assembled before a lawyer is paid to assemble it.",
    ]),
    ("h2", "What it does not do"),
    ("p", "It makes no statements about people: no scores on tenants, no predictions about who will "
          "pay. Files on buildings, contracts and cases only. It writes nothing back into your "
          "property management system unless you ask for that and the rules allow it. And it decides "
          "nothing; a person reads the file and acts."),
    ("h2", "How it would start with you"),
    ("p", "With one real object or one real dispute, from your own archive, under a data-processing "
          "agreement. You judge the result on a case whose answer you already know, which is the only "
          "honest way to test a colleague like this."),
    ("p", "The first phase leaves you with your files converted into a checked, machine-readable "
          "archive, yours whatever you decide afterwards. Property portfolios are exactly the kind of "
          "paper that will have to be converted sooner or later, and doing it on a small contract "
          "against real cases is the cheapest way to have it behind you."),
    ("p", "Frida, the document colleague, is in preparation and the first client engagement is being "
          "prepared now. Whoever writes now has a say in which files she works on first."),
]

LAW_ACCOUNTING = [
    ("h2", "The problem in this trade"),
    ("p", "The file is the work. A case arrives with years of correspondence, drafts that look alike, "
          "an engagement letter somewhere, invoices that belong to phases, and a client who remembers "
          "an assurance that may or may not be in writing. Reading it all is billable only in theory; "
          "in practice it happens at the end of the day, by the person who can least afford it."),
    ("h2", "What the colleague does with it"),
    ("ul", [
        "<b>The whole matter, in order.</b> Every document and message in a case, dated, across the "
        "archives the matter touches.",
        "<b>The wording that governs, quoted.</b> Which version of a clause is the operative one and "
        "what it actually says, verified word for word against the source before you see it.",
        "<b>Gaps stated as gaps.</b> No signed engagement letter, no written confirmation of an oral "
        "assurance, a missing appendix: named from the register of what was read.",
        "<b>A defensible trail.</b> Every statement carries a link to the original, so the reasoning "
        "can be checked by someone who was not in the room.",
    ]),
    ("h2", "Confidentiality and the boundary"),
    ("p", "Documents are processed in Europe under a data-processing agreement with Axon Trade ApS, "
          "and the supervisor that improves the colleague overnight sees no document and no name. "
          "Only the archives you put in scope are read, and nothing is read before you have agreed in "
          "writing."),
    ("p", "The colleague never judges people and never advises. It lays out what the documents say and "
          "what they do not. The professional judgement stays where it belongs, and so does the "
          "responsibility."),
    ("h2", "How it would start with you"),
    ("p", "One closed matter you know inside out, read from your own archive, so you can hold the "
          "result against what you already know. A small first contract, and you keep the converted "
          "archive whatever you decide afterwards: a checked, machine-readable form of your own files "
          "that any AI you adopt in the coming years will need anyway, and that nobody escapes "
          "building eventually."),
    ("p", "Frida is in preparation, with the first client engagement being prepared now."),
]

def page(slug, lang, family, title, h1, eyebrow, description, lede, priority, **extra):
    entry = {"slug": slug, "lang": lang, "family": family, "title": title, "h1": h1,
             "eyebrow": eyebrow, "description": description, "lede": lede, "priority": priority}
    entry.update(extra)
    return entry


PAGES = [
    # ------------------------------------------------------------- English
    page("how-it-works", "en", "how",
         "How a document colleague works · Neural Logic", "How a document colleague works.",
         "How it works",
         "A copy of your archives, converted into a checked and addressable form; a register of "
         "what every document contains; the complete file for any case, quoted word for word, "
         "with the gaps named. Processed in Europe.",
         "No migration, no new system to move into. A copy of the archives you already keep, read "
         "once and properly, so that any case can be laid out in full, quoted from the source, and "
         "honest about what is missing.",
         "0.9", blocks=HOW_IT_WORKS),
    page("questions", "en", "questions",
         "Questions and answers · Neural Logic", "Questions we are asked.", "Questions and answers",
         "Straight answers about Neural Logic: what a document colleague delivers, whether data "
         "leaves Europe, what happens when something is not in the files, who you sign with, what "
         "a first engagement looks like and what it costs.",
         "The questions that come up before anyone signs anything, answered as plainly as we can "
         "put them.",
         "0.9", qa=QUESTIONS),
    page("for/property-and-asset-management", "en", "property",
         "For property and asset management · Neural Logic", "For property and asset management.",
         "Where this fits",
         "A document colleague for property and asset managers: the complete file for a property, "
         "lease or dispute, assembled across data room, mail archive and shared drive, quoted from "
         "the source, with the missing protocol named.",
         "Everything about one property, one tenancy or one dispute, assembled across every "
         "archive you keep, quoted from the original, and clear about what was never filed.",
         "0.8", blocks=PROPERTY),
    page("for/law-and-accounting", "en", "law",
         "For law and accounting practices · Neural Logic", "For law and accounting practices.",
         "Where this fits",
         "A document colleague for practices whose work is the file: the whole matter in date "
         "order, the operative wording quoted and verified, gaps stated as gaps, and every "
         "statement traceable to its source. Processed in Europe.",
         "The whole matter in date order, the wording that governs quoted and checked against the "
         "source, and the missing engagement letter named rather than assumed.",
         "0.8", blocks=LAW_ACCOUNTING),
    page("archive-conversion", "en", "conversion",
         "Make your archive machine-readable · Neural Logic", "Make your archive machine-readable.",
         "Archive conversion",
         "Contracts, protocols, mail threads and scans converted into a checked, machine-readable "
         "archive with a register of what each document contains and what is missing. Yours to "
         "keep, usable by any language model, processed in Europe.",
         "Your contracts, protocols, mail threads and scans are readable by people and opaque to "
         "machines. Converting them is the slow part of every AI project, and it is work you will "
         "have to do whoever you eventually hire.",
         "0.9", blocks=CONVERSION_EN,
         service="Archive conversion: a company's documents read once and turned into a checked, "
                 "machine-readable archive with a register and a glossary, in open formats the "
                 "client keeps."),
    # -------------------------------------------------------------- German
    page("de/so-funktioniert-es", "de", "how",
         "So arbeitet eine Dokumenten-Kollegin · Neural Logic",
         "So arbeitet eine Dokumenten-Kollegin.", "So funktioniert es",
         "Eine Kopie Ihrer Archive wird zu einem geprüften Archiv mit Adressen, dazu ein Register, "
         "das festhält, was in jedem Dokument steht. Zu jedem Vorgang die vollständige Akte, wörtlich "
         "zitiert, Lücken beim Namen genannt. Verarbeitet in Europa.",
         "Keine Migration, kein neues System. Eine Kopie der Archive, die Sie ohnehin haben, einmal "
         "gründlich gelesen. Danach lässt sich jeder Vorgang vollständig aufblättern, aus der Quelle "
         "zitieren, und was fehlt, steht dabei.",
         "0.9", blocks=HOW_IT_WORKS_DE),
    page("de/fragen", "de", "questions",
         "Fragen und Antworten · Neural Logic", "Was wir gefragt werden.",
         "Fragen und Antworten",
         "Klare Antworten zu Neural Logic: was eine Dokumenten-Kollegin liefert, ob Daten Europa "
         "verlassen, was passiert, wenn etwas nicht in den Akten steht, mit wem Sie den Vertrag "
         "schließen, wie eine erste Zusammenarbeit aussieht und was sie kostet.",
         "Die Fragen, die vor jeder Unterschrift kommen. So klar beantwortet, wie wir können.",
         "0.9", qa=QUESTIONS_DE),
    page("de/fuer/immobilienverwaltung", "de", "property",
         "Für Immobilien- und Vermögensverwaltung · Neural Logic",
         "Für Immobilien- und Vermögensverwaltung.", "Wo das passt",
         "Eine Dokumenten-Kollegin für die Immobilien- und Vermögensverwaltung: die vollständige "
         "Akte zu einer Liegenschaft, einem Mietvertrag oder einem Streitfall, aus Datenraum, "
         "Mailarchiv und Netzlaufwerk zusammengestellt, aus der Quelle zitiert, das fehlende "
         "Protokoll beim Namen genannt.",
         "Alles zu einer Liegenschaft, einem Mietverhältnis oder einem Streitfall, aus allen Ihren "
         "Archiven zusammengetragen, im Original zitiert. Und klar gesagt, was nie abgelegt wurde.",
         "0.8", blocks=PROPERTY_DE),
    page("de/fuer/kanzleien", "de", "law",
         "Für Kanzleien und Steuerberatung · Neural Logic", "Für Kanzleien und Steuerberatung.",
         "Wo das passt",
         "Eine Dokumenten-Kollegin für Kanzleien, deren Arbeit die Akte ist: das ganze Mandat "
         "chronologisch, der maßgebliche Wortlaut zitiert und geprüft, Lücken als Lücken benannt, "
         "jede Aussage bis zur Quelle nachvollziehbar. Verarbeitet in Europa.",
         "Das ganze Mandat in chronologischer Reihenfolge, der geltende Wortlaut zitiert und an der "
         "Quelle geprüft. Und die fehlende Mandatsvereinbarung benannt, statt stillschweigend "
         "vorausgesetzt.",
         "0.8", blocks=LAW_DE),
    page("de/archiv-konvertierung", "de", "conversion",
         "Ihr Archiv maschinenlesbar machen · Neural Logic", "Ihr Archiv maschinenlesbar machen.",
         "Archivkonvertierung",
         "Verträge, Protokolle, Mailverläufe und Scans werden zu einem geprüften, maschinenlesbaren "
         "Archiv, dazu ein Register, das festhält, was in jedem Dokument steht und was fehlt. Es "
         "gehört Ihnen, funktioniert mit jedem Sprachmodell und wird in Europa verarbeitet.",
         "Ihre Verträge, Protokolle, Mailverläufe und Scans kann jeder Mensch lesen. Eine Maschine "
         "nicht. Sie zu konvertieren ist der langsame Teil jedes KI-Projekts, und diese Arbeit fällt "
         "an, egal wen Sie am Ende damit beauftragen.",
         "0.9", blocks=CONVERSION_DE,
         service="Archivkonvertierung: die Dokumente eines Unternehmens werden einmal gelesen und "
                 "in ein geprüftes, maschinenlesbares Archiv mit Register und Glossar überführt, "
                 "in offenen Formaten, die dem Kunden gehören."),
    # -------------------------------------------------------------- Danish
    page("da/saadan-virker-det", "da", "how",
         "Sådan arbejder en dokumentkollega · Neural Logic", "Sådan arbejder en dokumentkollega.",
         "Sådan virker det",
         "En kopi af dine arkiver bliver til et kontrolleret arkiv med adresser, plus et register "
         "over, hvad hvert dokument indeholder. Den komplette sag, uanset hvad du spørger om, citeret ord for ord, "
         "hullerne nævnt ved navn. Behandlet i Europa.",
         "Ingen migrering, intet nyt system. En kopi af de arkiver, du har i forvejen, læst grundigt "
         "én gang. Derefter kan enhver sag foldes helt ud, citeres fra kilden, og det, der mangler, "
         "står der også.",
         "0.9", blocks=HOW_IT_WORKS_DA),
    page("da/spoergsmaal", "da", "questions",
         "Spørgsmål og svar · Neural Logic", "Det, vi bliver spurgt om.", "Spørgsmål og svar",
         "Klare svar om Neural Logic: hvad en dokumentkollega leverer, om data forlader Europa, "
         "hvad der sker, når noget ikke står i sagerne, hvem du skriver kontrakt med, hvordan et "
         "første forløb ser ud, og hvad det koster.",
         "De spørgsmål, der kommer før enhver underskrift. Besvaret så ligeud, som vi kan.",
         "0.9", qa=QUESTIONS_DA),
    page("da/for/ejendomsadministration", "da", "property",
         "Til ejendomsadministration og asset management · Neural Logic",
         "Til ejendomsadministration og asset management.", "Hvor det passer ind",
         "En dokumentkollega til ejendomsadministration og asset management: den komplette sag om "
         "en ejendom, et lejemål eller en tvist, samlet fra datarum, mailarkiv og fællesdrev, "
         "citeret fra kilden, den manglende protokol nævnt ved navn.",
         "Alt om én ejendom, ét lejeforhold eller én tvist, samlet fra alle dine arkiver, citeret "
         "fra originalen. Og sagt klart, hvad der aldrig blev arkiveret.",
         "0.8", blocks=PROPERTY_DA),
    page("da/for/advokater-og-revisorer", "da", "law",
         "Til advokat- og revisionsvirksomheder · Neural Logic",
         "Til advokat- og revisionsvirksomheder.", "Hvor det passer ind",
         "En dokumentkollega til virksomheder, hvor sagen er arbejdet: hele sagen kronologisk, den "
         "gældende ordlyd citeret og kontrolleret, huller nævnt som huller, hvert udsagn sporbart "
         "til sin kilde. Behandlet i Europa.",
         "Hele sagen i kronologisk orden, den gældende ordlyd citeret og kontrolleret mod kilden. "
         "Og det manglende aftalebrev nævnt, i stedet for stiltiende forudsat.",
         "0.8", blocks=LAW_DA),
    page("da/arkiv-konvertering", "da", "conversion",
         "Gør jeres arkiv maskinlæsbart · Neural Logic", "Gør jeres arkiv maskinlæsbart.",
         "Arkivkonvertering",
         "Kontrakter, referater, mailtråde og scanninger bliver til et kontrolleret, maskinlæsbart "
         "arkiv, plus et register over, hvad hvert dokument indeholder, og hvad der mangler. Det er "
         "dit, virker med enhver sprogmodel og behandles i Europa.",
         "Dine kontrakter, referater, mailtråde og scanninger kan ethvert menneske læse. En maskine "
         "kan ikke. At konvertere dem er den langsomme del af ethvert AI-projekt, og det arbejde "
         "skal gøres, uanset hvem du ender med at hyre.",
         "0.9", blocks=CONVERSION_DA,
         service="Arkivkonvertering: en virksomheds dokumenter læses én gang og bliver til et "
                 "kontrolleret, maskinlæsbart arkiv med register og glossar, i åbne formater som "
                 "kunden beholder."),
]

PUBLISHED = json.loads((ROOT / "build" / "published.json").read_text(encoding="utf-8"))["languages"]
# A language Lead has not released is written in the content files but not built, linked or
# offered: dropping it here keeps every downstream check honest. A review page that must show
# the unreleased text imports this module with NL_PREVIEW_ALL=1 and gets everything.
import os  # noqa: E402
if not os.environ.get("NL_PREVIEW_ALL"):
    PAGES = [page_ for page_ in PAGES if page_["lang"] in PUBLISHED]
else:
    PUBLISHED = ["en", "de", "da"]
LANGS = [code for code in ["en", "de", "da"] if code in PUBLISHED]
LABEL = {"en": "EN", "de": "DE", "da": "DA"}
HOME = {"en": "/", "de": "/de/", "da": "/da/"}

# The site navigation, per language, in the order the pages are meant to be read.
NAV = {
    "en": [("how-it-works", "How it works"), ("archive-conversion", "Archive conversion"),
           ("questions", "Questions"), ("for/property-and-asset-management", "Property"),
           ("for/law-and-accounting", "Law &amp; accounting")],
    "de": [("de/so-funktioniert-es", "So funktioniert es"), ("de/archiv-konvertierung", "Archivkonvertierung"),
           ("de/fragen", "Fragen"), ("de/fuer/immobilienverwaltung", "Immobilien"),
           ("de/fuer/kanzleien", "Kanzleien")],
    "da": [("da/saadan-virker-det", "Sådan virker det"), ("da/arkiv-konvertering", "Arkivkonvertering"),
           ("da/spoergsmaal", "Spørgsmål"), ("da/for/ejendomsadministration", "Ejendomme"),
           ("da/for/advokater-og-revisorer", "Advokater &amp; revisorer")],
}

# The "read next" cards under each page, per family and language: (family, title, blurb).
NEXT = {
    "en": {
        "how": [("questions", "Questions and answers", "Data, liability, cost and what a first engagement looks like."),
                ("property", "For property and asset management", "The complete file for a property, a lease or a dispute.")],
        "questions": [("how", "How a document colleague works", "Conversion, the register, verified quotations, and the boundary."),
                      ("law", "For law and accounting practices", "The whole matter in order, with the wording that governs quoted.")],
        "property": [("how", "How a document colleague works", "What is handed over, what is built, what stays yours."),
                     ("conversion", "Make your archive machine-readable", "The first phase on its own: the groundwork, yours to keep.")],
        "law": [("conversion", "Make your archive machine-readable", "The first phase on its own: the groundwork, yours to keep."),
                ("questions", "Questions and answers", "Europe, liability, cost, and how a first phase runs.")],
        "conversion": [("how", "How a document colleague works", "What a colleague does once the archive can be read."),
                       ("questions", "Questions and answers", "Europe, liability, cost, and how a first phase runs.")],
    },
    "de": {
        "how": [("questions", "Fragen und Antworten", "Daten, Haftung, Kosten und wie eine erste Zusammenarbeit aussieht."),
                ("property", "Für Immobilien- und Vermögensverwaltung", "Die vollständige Akte zu einer Liegenschaft, einem Mietvertrag oder einem Streitfall.")],
        "questions": [("how", "So funktioniert eine Dokumenten-Kollegin", "Konvertierung, das Register, geprüfte Zitate und die Grenze."),
                      ("law", "Für Kanzleien und Steuerberatung", "Das ganze Mandat in Reihenfolge, mit dem maßgeblichen Wortlaut zitiert.")],
        "property": [("how", "So funktioniert eine Dokumenten-Kollegin", "Was übergeben wird, was entsteht, was Ihres bleibt."),
                     ("conversion", "Ihr Archiv maschinenlesbar machen", "Die erste Phase für sich: die Grundlage, die Ihnen gehört.")],
        "law": [("conversion", "Ihr Archiv maschinenlesbar machen", "Die erste Phase für sich: die Grundlage, die Ihnen gehört."),
                ("questions", "Fragen und Antworten", "Europa, Haftung, Kosten und wie eine erste Phase abläuft.")],
        "conversion": [("how", "So funktioniert eine Dokumenten-Kollegin", "Was eine Kollegin tut, sobald das Archiv lesbar ist."),
                       ("questions", "Fragen und Antworten", "Europa, Haftung, Kosten und wie eine erste Phase abläuft.")],
    },
    "da": {
        "how": [("questions", "Spørgsmål og svar", "Data, ansvar, pris og hvordan et første forløb ser ud."),
                ("property", "Til ejendomsadministration og asset management", "Den komplette sag for en ejendom, et lejemål eller en tvist.")],
        "questions": [("how", "Sådan virker en dokumentkollega", "Konvertering, registeret, kontrollerede citater og grænsen."),
                      ("law", "Til advokat- og revisionsvirksomheder", "Hele sagen i rækkefølge, med den gældende ordlyd citeret.")],
        "property": [("how", "Sådan virker en dokumentkollega", "Hvad der afleveres, hvad der bygges, hvad der forbliver jeres."),
                     ("conversion", "Gør jeres arkiv maskinlæsbart", "Den første fase i sig selv: grundarbejdet, som er jeres.")],
        "law": [("conversion", "Gør jeres arkiv maskinlæsbart", "Den første fase i sig selv: grundarbejdet, som er jeres."),
                ("questions", "Spørgsmål og svar", "Europa, ansvar, pris og hvordan en første fase forløber.")],
        "conversion": [("how", "Sådan virker en dokumentkollega", "Hvad en kollega gør, når arkivet kan læses."),
                       ("questions", "Spørgsmål og svar", "Europa, ansvar, pris og hvordan en første fase forløber.")],
    },
}

# Everything around the text of a page, per language.
CHROME = {
    "en": {"nav_label": "Pages", "lang_label": "Language", "contact_h": "Write to us.",
           "contact_p": "A description of the archives you hold and the question you would want "
                        "answered from them is enough to start a useful conversation.",
           "footer_left": "© Axon Trade ApS · Neural Logic · CVR 45 92 07 63",
           "footer_right": "Copenhagen · "},
    "de": {"nav_label": "Seiten", "lang_label": "Sprache", "contact_h": "Schreiben Sie uns.",
           "contact_p": "Sagen Sie uns, welche Archive Sie haben und was Sie daraus beantwortet "
                        "haben möchten. Mehr braucht es für ein gutes Gespräch nicht. Wir arbeiten "
                        "auf Deutsch, Dänisch und Englisch.",
           "footer_left": "© Axon Trade ApS · Neural Logic · CVR 45 92 07 63",
           "footer_right": "Kopenhagen · "},
    "da": {"nav_label": "Sider", "lang_label": "Sprog", "contact_h": "Skriv til os.",
           "contact_p": "Fortæl os, hvilke arkiver du har, og hvad du gerne vil have svar på ud "
                        "fra dem. Mere skal der ikke til for en god samtale. Vi arbejder på dansk, "
                        "tysk og engelsk.",
           "footer_left": "© Axon Trade ApS · Neural Logic · CVR 45 92 07 63",
           "footer_right": "København · "},
}

# ---------------------------------------------------------------- rendering

BEACON = """<!-- Visitor counter, our own and cookieless: sends the page path, the referring site and the browser
     language to our own brain. No cookie, no identifier, no IP address stored; nothing personal, so the
     page needs no consent banner. Source: Supabase edge function web-hit. -->
<script>
(function () {
  try {
    var site = location.hostname.replace(/^www\\./, '');
    if (site !== 'neurallogic.dk' && site !== 'axontrade.dk') return;
    var first = false;
    try { if (!sessionStorage.getItem('nl_seen')) { sessionStorage.setItem('nl_seen', '1'); first = true; } } catch (e) {}
    var ref = '';
    try { if (document.referrer) ref = new URL(document.referrer).hostname; } catch (e) {}
    var body = JSON.stringify({ site: site, path: location.pathname, ref: ref,
      lang: (navigator.language || '').slice(0, 12), first: first });
    var url = 'https://xwdyziighsmwgbxukezb.supabase.co/functions/v1/web-hit';
    if (navigator.sendBeacon) navigator.sendBeacon(url, new Blob([body], { type: 'text/plain' }));
    else fetch(url, { method: 'POST', body: body, keepalive: true }).catch(function () {});
  } catch (e) {}
})();
</script>"""

ICON = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'>"
        "<rect width='32' height='32' rx='7' fill='%230B1F35'/>"
        "<circle cx='11' cy='16' r='6' fill='%239FD1E8'/>"
        "<circle cx='21.5' cy='16' r='6' fill='none' stroke='%239FD1E8' stroke-width='1.8'/></svg>")

ORG_REF = {"@id": f"{SITE}/#org"}
BY_FAMILY_LANG = {(p["family"], p["lang"]): p for p in PAGES}


def sisters(page):
    """The versions of this page in every language that is actually built, English first."""
    return [(code, BY_FAMILY_LANG[(page["family"], code)])
            for code in LANGS if (page["family"], code) in BY_FAMILY_LANG]


def render_blocks(blocks) -> str:
    out = []
    for kind, value in blocks:
        if kind == "h2":
            out.append(f"  <h2>{value}</h2>")
        elif kind == "p":
            out.append(f"  <p>{value}</p>")
        elif kind == "note":
            out.append(f'  <p class="note">{value}</p>')
        elif kind == "ul":
            items = "\n".join(f"    <li>{i}</li>" for i in value)
            out.append(f'  <ul class="dash">\n{items}\n  </ul>')
        else:
            sys.exit(f"ERROR: unknown block type {kind!r}")
    return "\n".join(out)


def render_qa(qa) -> str:
    out = ['<div class="qa">']
    for question, answers in qa:
        paragraphs = "\n".join(f"    <p>{a}</p>" for a in answers)
        out.append(f"  <div>\n    <h2>{question}</h2>\n{paragraphs}\n  </div>")
    out.append("</div>")
    return "\n".join(out)


def structured_data(page) -> str:
    import re
    url = f"{SITE}/{page['slug']}/"
    lang = page["lang"]
    name = page["title"].split(" · ")[0]
    graph = [{
        "@type": "WebPage", "@id": url + "#page", "url": url, "name": name,
        "description": page["description"],
        "isPartOf": {"@id": f"{SITE}/#website"},
        "about": ORG_REF, "publisher": ORG_REF, "inLanguage": lang,
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Neural Logic", "item": SITE + HOME[lang]},
                {"@type": "ListItem", "position": 2, "name": name, "item": url},
            ]},
    }]
    if page.get("service"):
        graph.append({
            "@type": "Service", "@id": url + "#service",
            "name": page["h1"].rstrip("."), "description": page["service"],
            "provider": ORG_REF, "areaServed": ["DK", "DE", "EU"],
            "serviceType": "Document archive conversion", "inLanguage": lang,
            "termsOfService": "Processed in Europe under a data-processing agreement; the converted "
                              "archive, the register and the glossary stay the client's.",
        })
    if page.get("qa"):
        graph.append({
            "@type": "FAQPage", "@id": url + "#faq",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", " ".join(a))}}
                for q, a in page["qa"]],
        })
    return json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, separators=(",", ":"))


def render_page(page) -> str:
    slug, lang = page["slug"], page["lang"]
    chrome = CHROME[lang]
    url = f"{SITE}/{slug}/"
    current = ' aria-current="page"'

    nav = "\n".join(
        '      <a href="/{}/"{}>{}</a>'.format(s, current if s == slug else "", label)
        for s, label in NAV[lang])

    group = sisters(page)
    chooser = ""
    if len(group) > 1:
        links = "".join(
            '<a href="/{}/" hreflang="{}" lang="{}"{}>{}</a>'.format(
                p["slug"], code, code, current if code == lang else "", LABEL[code])
            for code, p in group)
        chooser = f'\n  <nav class="langs" aria-label="{chrome["lang_label"]}">{links}</nav>'
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{code}" href="{SITE}/{p["slug"]}/">' for code, p in group)
    if len(group) > 1:
        alternates += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}/{group[0][1]["slug"]}/">'

    main = render_qa(page["qa"]) if page.get("qa") else render_blocks(page["blocks"])
    cards = "\n".join(
        '  <a href="/{}/"><span class="t">{}</span><span class="d">{}</span></a>'.format(
            BY_FAMILY_LANG[(fam, lang)]["slug"], t, d)
        for fam, t, d in NEXT[lang][page["family"]])

    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{page['title']}</title>
<meta name="description" content="{html.escape(page['description'], quote=True)}">
<meta property="og:title" content="{html.escape(page['title'].split(' · ')[0], quote=True)}">
<meta property="og:description" content="{html.escape(page['description'], quote=True)}">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:url" content="{url}">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{url}">
{alternates}
<link rel="icon" href="{ICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600&display=swap" onload="this.onload=null;this.rel='stylesheet'"><noscript><link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600&display=swap" rel="stylesheet"></noscript>
<link rel="stylesheet" href="/pages.css">
<script type="application/ld+json">
{structured_data(page)}
</script>
</head>
<body>
<header class="top"><div class="wrap">
  <a class="mark" href="{HOME[lang]}">Neural Logic</a>
  <nav aria-label="{chrome['nav_label']}">
{nav}
  </nav>{chooser}
</div></header>

<main><div class="wrap">
  <h1>{page['h1']}</h1>
  <p class="lede">{page['lede']}</p>

  <div class="body">
{main}
  </div>

  <div class="contact">
    <h2>{chrome['contact_h']}</h2>
    <p>{chrome['contact_p']}</p>
    <a class="mail" href="mailto:info@neurallogic.dk">info@neurallogic.dk</a>
  </div>

  <div class="next">
{cards}
  </div>
</div></main>

<footer class="foot"><div class="wrap">
  <span>{chrome['footer_left']}</span>
  <span>{chrome['footer_right']}<a href="mailto:info@neurallogic.dk">info@neurallogic.dk</a></span>
</div></footer>
{BEACON}
</body>
</html>
"""


def write_sitemap() -> None:
    """One entry per page and language, each carrying its language equivalents (xhtml:link),
    exactly the alternates the pages themselves declare. Families sorted by priority, English first."""
    families = [({code: HOME[code] for code in LANGS}, "1.0")]
    for p in sorted((p for p in PAGES if p["lang"] == "en"), key=lambda p: -float(p["priority"])):
        families.append(({code: "/" + BY_FAMILY_LANG[(p["family"], code)]["slug"] + "/"
                          for code in LANGS if (p["family"], code) in BY_FAMILY_LANG}, p["priority"]))
    entries, count = [], 0
    for urls, priority in families:
        alts = "".join(
            f'\n    <xhtml:link rel="alternate" hreflang="{code}" href="{SITE}{path}"/>'
            for code, path in [*urls.items(), ("x-default", urls["en"])])
        for path in urls.values():
            entries.append(f"  <url>\n    <loc>{SITE}{path}</loc>{alts}\n    <priority>{priority}</priority>\n  </url>")
            count += 1
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(entries) + "\n</urlset>\n", encoding="utf-8")
    return count


def check() -> None:
    """Never link to a page that is not built: navigation, cards and sisters all resolve."""
    built = {p["slug"] for p in PAGES}
    for lang, entries in NAV.items():
        if lang not in LANGS:
            continue                      # written, not released: nothing of it is built or linked
        missing = [s for s, _label in entries if s not in built]
        if missing:
            sys.exit(f"ERROR: navigation for {lang!r} names pages that are not built: {missing}")
    for lang, fams in NEXT.items():
        if lang not in LANGS:
            continue
        for fam, cards in fams.items():
            for target, _t, _d in cards:
                if (target, lang) not in BY_FAMILY_LANG:
                    sys.exit(f"ERROR: a card on the {fam!r} page ({lang}) points at {target!r}, "
                             f"which is not built in {lang}")
    for p in PAGES:
        if (p["family"], p["lang"]) != (p["family"], p["lang"]) or not p.get("blocks", p.get("qa")):
            sys.exit(f"ERROR: page {p['slug']} has no content")


def main() -> None:
    check()
    for page_ in PAGES:
        target = ROOT / page_["slug"] / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_page(page_), encoding="utf-8")
        print("wrote", target.relative_to(ROOT))
    print("wrote sitemap.xml with", write_sitemap(), "addresses")


if __name__ == "__main__":
    main()
