import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, EventEmitter, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { environment } from 'src/environments/environment';
import { IUser } from '../../state/objects';
import { Store } from '@ngxs/store';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
    @Output() success = new EventEmitter<string>();

    public name: string;

    public loginForm: FormGroup;
    public loginFailed = false;
    public get emailControl() {
        return this.loginForm?.get('email');
    }
    public get passwordControl() {
        return this.loginForm?.get('password');
    }

    constructor(
        private httpClient: HttpClient,
        private cookiesService: CookieService,
        private router: Router,
        private store: Store
    ) {
        this.loginForm = new FormGroup({
            email: new FormControl('', Validators.required),
            password: new FormControl('', Validators.required),
        });
    }

    public sbumit() {
        const headers = new HttpHeaders();
        headers.set('Content-Type', 'application/json');
        this.httpClient
            .post<{
                user: IUser;
                access_token: string;
            }>(
                `${environment.backendUrl}/auth/login`,
                {
                    email: this.loginForm.value.email,
                    password: this.loginForm.value.password,
                },
                {
                    headers,
                    withCredentials: true,
                    observe: 'response',
                }
            )
            .subscribe((response) => {
                if (response.status === 200) {
                    if (response.body.access_token) {
                        this.loginFailed = false;
                        this.cookiesService.set('token', response.body.access_token);
                        this.router.navigate([''], { replaceUrl: true });
                    } else {
                        this.loginFailed = true;
                    }
                }
            });
    }
}
