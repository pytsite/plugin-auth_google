/**
 * While writing code for this widget, refer to https://developers.google.com/identity/sign-in/web/reference
 */
define(['jquery', 'assetman', 'pytsite-auth-http-api', 'pytsite-google'], function ($, assetman, pytsiteAuth, google) {
    return function (widget) {
        google.ready(function (gapi) {
            gapi.load('auth2', function () {
                gapi.auth2.init().then(function () {
                    var googleAuthInstance = gapi.auth2.getAuthInstance();

                    pytsiteAuth.isAnonymous().done(function (isAnonymous) {
                        if (isAnonymous) {
                            // Sign out from Google and render "Sign In" button
                            googleAuthInstance.signOut();
                            gapi.signin2.render(widget.uid, {
                                onSuccess: function (user) {
                                    var form = $('.pytsite-auth-sign-in.driver-google');
                                    form.find('input[id$="id-token"]').val(user.getAuthResponse().id_token);
                                    form.submit();
                                }
                            });
                        }
                        else {
                            console.log("Already authorized");
                        }
                    });
                });
            });
        });


        assetman.loadCSS('plugins.auth_google@css/auth-google-widget.css');
    }
});
