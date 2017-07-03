/**
 * While writing code for this widget, refer to https://developers.google.com/identity/sign-in/web/reference
 */
define(['jquery', 'assetman', 'pytsite-auth-http-api'], function ($, assetman, pytsiteAuth) {
    return function (widget) {
        function onAuthGoogleSignIn(user) {
            var form = $('.pytsite-auth-sign-in.driver-google');
            form.find('input[id$="id-token"]').val(user.getAuthResponse().id_token);
            form.submit();
        }

        window.onGAPILoad = function () {
            gapi.load('auth2', function () {
                var auth = gapi.auth2.init({
                    client_id: widget.em.data('clientId')
                });

                auth.then(function () {
                    var auth = gapi.auth2.getAuthInstance();

                    // First, check if the Google's user is authenticated in PytSite
                    pytsiteAuth.isAnonymous().done(function (isAnonymous) {
                        if (isAnonymous) {
                            // Sign out from Google and render "Sign In" button
                            auth.signOut();
                            gapi.signin2.render(widget.uid, {
                                onSuccess: onAuthGoogleSignIn
                            });
                        }
                        else {
                            console.log("Already authorized");
                        }
                    });
                });
            });
        };

        assetman.loadCSS('plugins.auth_google@css/auth-google-widget.css');
        assetman.loadJS('https://apis.google.com/js/platform.js?onload=onGAPILoad');
    }
});
