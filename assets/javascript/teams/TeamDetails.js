'use strict';
import React, {useEffect, useState,} from "react";
import {Link} from "react-router-dom";
import {TeamMemberList} from "./TeamMembers";
import {InvitationList} from "./Invitations";
import ValidationErrors from "../utilities/ValidationErrors";


const TeamDetails = function(props) {
  const [name, setName] = useState(props.team?.name || "");
  const [slug, setSlug] = useState(props.team?.slug || "");
  const creatingNewTeam = !Boolean(props.team);
  const canEditTeam = creatingNewTeam ? true : props.team?.isAdmin;
  const useRouter = Boolean(props.returnUrl);

  const saveTeam = function(event) {
    props.save(props.team, name, slug);
    event.preventDefault();
  };

  const deleteTeam = function(event) {
    props.delete(props.team);
    event.preventDefault();
  };

  const renderIdField = function() {
    if (!creatingNewTeam) {
      return (
        <div className="pg-input-group">
          <label className="pg-label">{gettext("Team ID")}</label>
          <input className="pg-control" type="text" placeholder="dunder-mifflin"
                 onChange={(event) => setSlug(event.target.value)} value={slug} disabled={!canEditTeam}>
          </input>
          <p className="pg-help form-text">{gettext("A unique ID for your team. No spaces are allowed!")}</p>
          <ValidationErrors errors={props.errors?.slug} />
        </div>
      );
    }
  };

  const renderCancel = function() {
    if (useRouter) {
      return (
        <Link to={props.returnUrl}>
          <button className="pg-button-light mx-2">
            <span>{gettext("Cancel")}</span>
          </button>
        </Link>
      );
    } else {
      // when not using the router there's no need for a "cancel" button
      return '';
    }
  };

  const getSaveButtonText = () => {
    if (props.recentlySaved) {
      return "Saved!";
    } else {
      return creatingNewTeam ? gettext('Add Team') : gettext('Save Details');
    }
  };
  const renderDetails = function() {
    return (
      <section className="app-card">
        <form>
          <h3 className="pg-subtitle">{gettext("Team Details")}</h3>
          <div className="pg-input-group">
            <label className="pg-label">{gettext("Team Name")}</label>
            <input className="pg-control" type="text" placeholder="Dunder Mifflin"
                   onChange={(event) => setName(event.target.value)} value={name}
                   disabled={!canEditTeam}>
            </input>
            <p className="pg-help form-text">{gettext("Your team name.")}</p>
            <ValidationErrors errors={props.errors?.name} />
          </div>
          {renderIdField()}
          {canEditTeam ? (
            <div className="pg-inline-buttons">
              <button className={creatingNewTeam ? 'pg-button-primary' : 'pg-button-secondary'}
                      onClick={saveTeam}>
                              <span className="pg-icon">
                                  <i className={`fa ${creatingNewTeam ? 'fa-plus' : 'fa-check'}`}></i>
                              </span>
                <span>{getSaveButtonText()}</span>
              </button>
              {renderCancel()}
            </div>
            ) : ''}
        </form>
      </section>
    );
  };

  const renderMembers = function() {
    if (creatingNewTeam) {
      return null;
    } else {
      return (
        <TeamMemberList
          apiUrls={props.apiUrls}
          team={props.team}
          members={props.team.members}
          user={props.user}
        />
      );
    }
  };

  const renderInvitations = function() {
    if (creatingNewTeam) {
      return null;
    } else {
      return (
        <InvitationList team={props.team} client={props.client} canManageInvitations={canEditTeam}
                        apiUrls={props.apiUrls}/>
      );
    }
  };

  const renderDeleteModal = function () { 
      return <div className="modal" tabIndex="-1" id="delete-team-modal">
        <div className="modal-dialog modal-dialog-centered">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">{gettext("Really delete team?")}</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label={gettext("Close")}></button>
            </div>
            <div className="modal-body">
              {gettext("This will permanently delete the team and all associated data:")}
              <em><strong>{name}</strong></em><br/>
              <strong>{gettext("This action cannot be undone.")}</strong>
            </div>
            <div className="modal-footer">
              <button className="btn btn-danger" data-bs-dismiss="modal" onClick={deleteTeam}>
                {gettext("I understand, permanently delete this team")}
              </button>
              <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">{gettext("Cancel")}</button>
            </div>
          </div>
        </div>
      </div>
  };

  const renderDangerZone = function() {
    if (creatingNewTeam || !canEditTeam) {
      return "";
    } else {
      return <>
        <section className="app-card">
          <h3 className="pg-subtitle">{gettext("Danger Zone")}</h3>
            <button className="pg-button-danger" type="button" data-bs-toggle="modal" data-bs-target="#delete-team-modal">
              {gettext("Delete Team")}
            </button>
        </section>
        {renderDeleteModal()}
      </>
    }
  };

  return (
    <div>
      {renderDetails()}
      {renderMembers()}
      {renderInvitations()}
      {renderDangerZone()}
    </div>
  );

};


export default TeamDetails;
