import { HttpClient } from '@angular/common/http';
import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, ValidationErrors, Validators } from '@angular/forms';
import { IUser } from 'src/app/state/objects';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-jobs',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss'],
})
export class UsersComponent implements OnInit, OnDestroy {

  public users: IUser[];
  public editForm: FormGroup;
  public editVisible = false;
  public editMode: 'create' | 'update';

  private url = `${environment.backendUrl}/user`;

  constructor(private httpClient: HttpClient) {
    this.editForm = new FormGroup({
      email: new FormControl('', Validators.required),
        firstname: new FormControl('', Validators.required),
        lastname: new FormControl('', Validators.required),
        password: new FormControl('', Validators.required),
        passwordRepeat: new FormControl('', Validators.required),
        isAdmin: new FormControl(false),
    });
  }

  @HostListener('window:beforeunload', ['$event']) unloadHandler(event: Event) {
    this.saveState();
  }

  public ngOnInit(): void {
    this.loadState();
    this.loadUser();
  }

  public ngOnDestroy(): void {
    this.saveState();
  }

  public loadUser() {
    this.httpClient.get<{ users: IUser[] }>(
      `${environment.backendUrl}/user`,
      {
        observe: 'response',
        withCredentials: true
      }
    ).subscribe(s => {
      this.users = s.body.users;
      if (this.editVisible && this.editMode === 'update') {
        const user = this.users.find(({email}) => email === this.editForm.value.email );
        if (user) {
          this.editForm.setValue({
            email: user.email,
            firstname: user.firstname,
            lastname: user.lastname,
            password: '',
            passwordRepeat: '',
            isAdmin: user.isAdmin
          });
        } else {
          this.editVisible = false;
        }
      };
    });
  }

  public delete(email: string) {
    if (confirm(`Delete user: ${email}?`)) {
      this.httpClient.delete(
        `${environment.backendUrl}/user/${email}`,
        {
          observe: 'response',
          withCredentials: true
        }
      ).subscribe(s => {
        this.loadUser();
      });
    }
  }

  public create() {
    this.editForm.setValidators([this.passwordsMatch]);
    this.editForm.setValue({
      email: '',
      firstname: '',
      lastname: '',
      password: '',
      passwordRepeat: '',
      isAdmin: ''
    });
    this.editMode = 'create';
    this.editVisible = true;
  }

  public update(user) {
    this.editForm.setValidators([]);
    this.editForm.setValue({
      email: user.email,
      firstname: user.firstname,
      lastname: user.lastname,
      password: '',
      passwordRepeat: '',
      isAdmin: user.isAdmin
    });
    this.editMode = 'update';
    this.editVisible = true;
  }

  public submit() {
    if (this.editMode === 'update') {
      this.httpClient.put(
        `${this.url}/${this.editForm.get('email').value}`,
        this.editForm.value,
        {
          observe: 'response',
          withCredentials: true
        }
      ).subscribe(() => {
        this.editVisible = false;
        this.loadUser();
      });
    } else if (this.editMode === 'create') {
      this.httpClient.post(
        `${this.url}`,
        this.editForm.value,
        {
          observe: 'response',
          withCredentials: true
        }
      ).subscribe(() => {
        this.editVisible = false;
        this.loadUser();
      });
    }
  }

  private passwordsMatch(form: FormGroup): ValidationErrors {
    if (form?.get('password')?.value === form?.get('passwordRepeat')?.value) {
      return null;
    } else {
      return { passwordNotMatch: true };
    }
  };

  private saveState() {
    const state = {
      editVisible: this.editVisible,
      editMode: this.editMode,
      formValue: this.editVisible ? this.editForm.value : null
    };
    localStorage.setItem('usersPageState', JSON.stringify(state));
  }

  private loadState() {
    const state = JSON.parse(localStorage.getItem('usersPageState'));
    this.editVisible = state.editVisible;
    this.editMode = state.editMode;
    if (this.editVisible) {
      this.editForm.setValue(state.formValue);
    };
  }
}
