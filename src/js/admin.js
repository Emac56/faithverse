import { supabase } from './supabase.js'

const totalUsers =
    document.getElementById('totalUsers')

const totalPrayers =
    document.getElementById('totalPrayers')

const totalVerses =
    document.getElementById('totalVerses')

const totalCategories =
    document.getElementById('totalCategories')

const recentActivity =
    document.getElementById('recentActivity')

async function checkAdmin() {

    const {
        data: { session }
    } = await supabase.auth.getSession()

    if (!session) {

        window.location.href =
            '/admin/login.html'

        return
    }

    const { data: admin } =
        await supabase
            .from('admins')
            .select('*')
            .eq('id', session.user.id)
            .single()

    if (!admin) {

        await supabase.auth.signOut()

        window.location.href =
            '/admin/login.html'
    }
}

async function loadAnalytics() {

    const {
        count: usersCount
    } = await supabase
        .from('users')
        .select('*', {
            count: 'exact',
            head: true
        })

    const {
        count: prayersCount
    } = await supabase
        .from('prayer_requests')
        .select('*', {
            count: 'exact',
            head: true
        })

    const {
        count: versesCount
    } = await supabase
        .from('verses')
        .select('*', {
            count: 'exact',
            head: true
        })

    const {
        count: categoriesCount
    } = await supabase
        .from('categories')
        .select('*', {
            count: 'exact',
            head: true
        })

    totalUsers.textContent =
        usersCount || 0

    totalPrayers.textContent =
        prayersCount || 0

    totalVerses.textContent =
        versesCount || 0

    totalCategories.textContent =
        categoriesCount || 0
}

async function loadRecentActivity() {

    const { data } =
        await supabase
            .from('prayer_requests')
            .select('*')
            .order('created_at', {
                ascending: false
            })
            .limit(5)

    recentActivity.innerHTML = ''

    data?.forEach((item) => {

        recentActivity.innerHTML += `

        <div class="rounded-2xl border border-white/10 p-5">

            <p class="font-semibold">
                ${item.name || 'Anonymous'}
            </p>

            <p class="mt-2 text-slate-400">
                ${item.message}
            </p>

        </div>

        `
    })
}

document
    .getElementById('logoutBtn')
    ?.addEventListener(
        'click',
        async () => {

            await supabase.auth.signOut()

            window.location.href =
                '/admin/login.html'
        }
    )

await checkAdmin()

await loadAnalytics()

await loadRecentActivity()
