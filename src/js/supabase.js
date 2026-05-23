import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm'

const SUPABASE_URL =
'https://dsqikxpizvtqnzchfznu.supabase.co'

const SUPABASE_ANON_KEY =
'sb_publishable_2x_PFhRWPNBirgQKCKIDDQ_wz-GCOLl'

export const supabase =
createClient(
    SUPABASE_URL,
    SUPABASE_ANON_KEY
)
