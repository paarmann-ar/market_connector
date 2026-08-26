
==================================================
 FOCUS KEYWORDS
==================================================

Create a concise bilingual focus keywords.
Put it in output json as value of focus_keywords.


Generate maximum 4 focus keywords in germany and Generate maximum 4 focus keywords in english.

If only 4 genuinely distinct search concepts are supported, generate only 4.

Each keyword must:

- be directly supported by PRODUCT DATA
- describe the exact product
- represent a distinct search concept
- be concise
- be useful for B2B industrial search
- be unique
- add meaningful search coverage

Preferred concepts:

1. Brand + model/part number
2. Product type + model/part number
3. Brand + product type
4. Product type + important technical specification
5. Exact technical product type

Use a concept only when it provides genuinely different search intent.

DO NOT:

- create duplicates
- change only word order
- create long and short versions of the same keyword
- repeat brand + model unnecessarily
- combine every product attribute into every keyword
- create generic keywords when an exact concept exists
- invent brands, models, specifications, applications, or product types

Distinctness test:

Compare every new keyword against existing keywords.

If two keywords essentially target the same search intent, keep only the stronger and more specific one.

Example VALID:

[
  "FITOK pressure relief valve",
  "High pressure relief valve",
  "HARSS-FH9-FNS12-2"
]

Example INVALID:

[
  "FITOK HARSS-FH9-FNS12-2 pressure relief valve",
  "FITOK HARSS-FH9-FNS12-2 high pressure relief valve",
  "FITOK HARSS-FH9-FNS12-2 valve"
]

==================================================
 PRIMARY FOCUS KEYWORD
==================================================

Select EXACTLY ONE primary focus keyword from focus_keywords just in english.
Put it in output json as value of primary_focus_keyword.


It MUST:

- exist exactly in focus_keywords
- be character-for-character identical
- describe the exact product
- be directly supported by PRODUCT DATA
- be the strongest commercially relevant search concept
- preferably include an exact model or part number when available

Do NOT translate, shorten, modify, reorder, capitalize differently, or otherwise alter it.

The primary focus keyword must appear naturally in:

1. title
2. description
3. meta_description

Because the title and meta_description are bilingual, the keyword may appear in the English portion when that is the natural placement.

Never force it unnaturally into German.

If the selected keyword cannot be used naturally in all required fields, select another keyword from focus_keywords.

==================================================
 SLUG
==================================================

Always generate the "slug" field just in english.
Put it in output json as value of slug.

The slug is REQUIRED.

The slug must:

- be short
- be SEO-friendly
- identify the exact product
- use lowercase English words, numbers, and valid model/part-number characters
- use hyphens between segments
- contain no spaces, underscores, HTML, or leading/trailing slash
- be based only on PRODUCT DATA
- not contain invented information

Preferred length:

- maximum 7 meaningful segments

Priority:

1. Brand + model/part number
2. Product type + model/part number
3. Brand + short product type
4. Short English product title

Keep the slug as short as possible while clearly identifying the exact product.

Prefer model/part number over unnecessary technical specifications.

Do NOT include:

- condition
- price
- sale
- new
- used
- buy
- shop
- product
- official
- best
- marketing terms

unless inseparable from the actual product name.

Do not include every technical specification.

Do not invent or translate model numbers or part numbers.

Only convert normal words to lowercase.

Example:
END-ARMATUREN EA 2-WAY BALL VALVE & ACTUATOR ZA310063-EE620632 DN20 PN64

Preferred:
"end-armaturen-za310063-ee620632"

Avoid:
"end-armaturen-ea-2-way-ball-valve-actuator-za310063-ee620632-dn20-pn64-stainless-steel"

The slug identifies the product; it does not describe every specification.

==================================================
 IMAGE DESCRIPTION
==================================================
Create exactly ONE bilingual Image description.
Put it in output json as value of image_description.

EXACT STRUCTURE:

German IMAGE DESCRIPTION | English IMAGE DESCRIPTION

Base it ONLY on information supported by PRODUCT DATA.

Generate a concise product-image description based on the exact product identity and supported product information.

Requirements:

- concise and natural
- useful for accessibility and image SEO
- product-specific
- include brand, product type, model, or part number when supported
- no invented colors, dimensions, materials, specifications, components, or visual details
- no marketing language
- no keyword stuffing
- no HTML or markdown
- do not start with "Bild von", "Foto von", or "Dieses Bild zeigt"

Maximum length is 30 words.

Example:

"END-ARMATUREN EA 2-Wege-Kugelhahn mit Antrieb, Modell ZA310063-EE620632 | END-ARMATUREN EA 2-Way-Ball Valve with actuator, model ZA310063-EE620632"

==================================================
 PRODUCT TAGS
==================================================

Create a concise bilingual product tags specifically for WooCommerce.
Put it in output json as value of product_tags.


Tags are NOT the same as focus_keywords.

Focus keywords are SEO search concepts.

Tags are short, reusable product attributes and search terms that can be used to group related products.

Extract tags ONLY from the PRODUCT DATA.

Tags may include:

- Brand
- Manufacturer
- Product type
- Product category
- Product-specific technical terms
- Model numbers
- MPN
- Article numbers
- Part numbers
- Product numbers
- Technical identifiers
- Important product-specific terminology

LANGUAGE:

For meaningful natural-language tags, provide both German and English versions as SEPARATE tags.

Example:

"Motor"
→ ["Motor", "Engine"]

"Ventil"
→ ["Ventil", "Valve"]

Do NOT combine translations into one tag.

Wrong:
"Motor | Engine"

Correct:
"Motor", "Engine"

For brands, model numbers, part numbers, article numbers, product numbers, and technical identifiers that do not require translation, return the value ONLY ONCE.

Example:

"Siemens"
→ ["Siemens"]

"ZA310063"
→ ["ZA310063"]

"EE620632"
→ ["EE620632"]

HYPHEN HANDLING:

Do NOT blindly split every expression containing "-".

Use the meaning and structure of the title to determine whether a hyphenated expression is:

1. One complete product/model identifier

or

2. Multiple independent technical identifiers.

If multiple independent identifiers are clearly present, return them as separate tags.

Example:

"Siemens ZA310063-EE620632 Motor"

→

[
  "Siemens",
  "ZA310063",
  "EE620632",
  "Motor",
  "Engine"
]

Do NOT return:

"ZA310063-EE620632"

when the context clearly indicates that ZA310063 and EE620632 are separate identifiers.

However, if the entire hyphenated expression is clearly one model or product identifier, preserve it as ONE tag.

Example:

"Bosch GSR 18V-55"

→

[
  "Bosch",
  "GSR 18V-55"
]

Do not split normal hyphenated product names unnecessarily.

Do NOT create tags for generic or commercially meaningless words such as:

- new
- neu
- used
- gebraucht
- original
- professional
- premium
- high quality
- excellent
- item
- product
- set
- offer
- sale

unless such a term is explicitly part of a meaningful official product name or identifier.

Do NOT create synonyms except for the required German/English translation pair.

Do NOT invent tags.

Do NOT infer tags from general knowledge.

Do NOT create generic category tags unless the category is explicitly supported by PRODUCT DATA.

Remove duplicate tags.

Keep tags concise.

Prefer specific and reusable tags over long phrases.

A tag should normally be a single meaningful concept rather than a complete SEO sentence.

Examples:

Siemens ZA310063-EE620632 Motor

[
  "Siemens",
  "ZA310063",
  "EE620632",
  "Motor",
  "Engine"
]

Bosch GSR 18V-55 Professional Akku-Bohrschrauber

[
  "Bosch",
  "GSR 18V-55",
  "Akku-Bohrschrauber",
  "Cordless drill"
]

Do NOT include focus keywords automatically.

Only include a focus keyword as a tag when the keyword itself is also a meaningful reusable product tags.

Return between 1 and 10 tags when meaningful tags exist.

If no meaningful tags can be identified, return an empty array.


**==================================================**
OUTPUT CONTRACT — HIGHEST PRIORITY
**==================================================**

The following JSON schema is the ONLY valid output schema.

Return exactly ONE JSON object containing EXACTLY these 9 keys:

{{
  "title": "",
  "description": "",
  "short_description": "",
  "meta_description": "",
  "focus_keywords": [],
  "primary_focus_keyword": "",
  "slug": "",
  "image_description": "",
  "product_tags": []
}}
