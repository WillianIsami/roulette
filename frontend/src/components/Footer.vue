<template>
    <div class="container">
        <footer class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
            <div class="col-md-4 d-flex align-items-center justify-content-center">
                <a href="/" class="text-muted text-decoration-none lh-1">
                    <img src="../assets/icons/logo.png" width="40" height="40"/>
                </a>
                <span class="ms-3 text-muted">© 2024 Company, Inc</span>
            </div>

            <div class="d-flex justify-content-end">
                <ul class="nav col-md-4 justify-content-end list-unstyled d-flex w-100">
                    <li class="ms-3"><a class="text-muted" href="#"><img src="../assets/icons/instagram.png" width="24" height="24" /></a></li>
                    <li class="ms-3"><a class="text-muted" href="#"><img src="../assets/icons/twitter.png" width="24" height="24" /></a></li>
                    <li class="ms-3"><a class="text-muted" href="#"><img src="../assets/icons/youtube.png" width="24" height="24" /></a></li>
                </ul>
            </div>
        </footer>
    </div>
</template>

<script>
    export default {
        name: 'FooterComponent',
    }
</script>
