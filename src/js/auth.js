import { supabase } from './supabase.js'

const loginForm =
    document.getElementById('loginForm')

async function loginAdmin(
    email,
    password
) {

    const { data, error } =
        await supabase.auth.signInWithPassword({
            email,
            password
        })

    if (error) {
        alert(error.message)
        return
    }

    const user = data.user

    const {
        data: adminData
    } = await supabase
        .from('admins')
        .select('*')
        .eq('id', user.id)
        .single()

    if (!adminData) {

        await supabase.auth.signOut()

        alert(
            'Unauthorized admin access'
        )

        return
    }

    localStorage.setItem(
        'faithverse_admin',
        JSON.stringify(adminData)
    )

    window.location.href =
        '/admin/dashboard.html'
}

loginForm?.addEventListener(
    'submit',
    async (e) => {

        e.preventDefault()

        const email =
            document.getElementById(
                'email'
            ).value

        const password =
            document.getElementById(
                'password'
            ).value

        await loginAdmin(
            email,
            password
        )
    }
)
