# Drug images — naming convention

One image per drug, named exactly by the drug's slug (see src/data_drugs.py):

  fentanyl.webp          <- drugs/fentanyl/
  alprazolam.webp        <- drugs/alprazolam/
  2f-dck.webp            <- drugs/2f-dck/   (slugs keep their hyphens)

Accepted formats: .webp (preferred), .jpg, .jpeg, .png
If a slug has no matching image here, the profile automatically falls
back to the clean placeholder — so you can add images incrementally.

Specs: 1200x630px (og:image ratio works for both card + share image),
under ~150 KB, no watermarks, no graphic injection imagery — product/
powder/blister-style shots or clean illustrations.
