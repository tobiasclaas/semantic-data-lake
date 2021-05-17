import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Store } from '@ngxs/store';
import { CookieService } from 'ngx-cookie-service';
import { environment } from 'src/environments/environment';
import { SetActiveUser } from '../../state/actions';

@Component({
    selector: 'app-jobs',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss'],
})
export class HomeComponent {

    constructor(
        private store: Store,
        private httpClient: HttpClient,
        private cookiesService: CookieService,
    ) { }


    logout() {
        if (confirm('logout?')) {
            this.httpClient
                .post(`${environment.backendUrl}/auth/logout`, '', { withCredentials: true })
                .subscribe(() => {
                    this.cookiesService.delete('token');
                    this.store.dispatch(new SetActiveUser(null));
                    window.location.reload();
                });
        }
    }
}
