"""
Skype4Py constants.

**Warning!** Remember that all constants defined here are available at
the `Skype4Py` package level and should be accessed from there.

Example:
   
.. python::

    import Skype4Py

    status = Skype4Py.apiAttachSuccess
"""
__docformat__ = 'restructuredtext en'


#{ Attachment status
apiAttachUnknown = -1
apiAttachSuccess = 0
apiAttachPendingAuthorization = 1
apiAttachRefused = 2
apiAttachNotAvailable = 3
apiAttachAvailable = 0x8001


#{ Connection status
conUnknown = 'UNKNOWN'
conOffline = 'OFFLINE'
conConnecting = 'CONNECTING'
conPausing = 'PAUSING'
conOnline = 'ONLINE'


#{ User status
cusUnknown = 'UNKNOWN'
cusOffline = 'OFFLINE'
cusOnline = 'ONLINE'
cusAway = 'AWAY'
cusNotAvailable = 'NA'
cusDoNotDisturb = 'DND'
cusInvisible = 'INVISIBLE'
cusLoggedOut = 'LOGGEDOUT'
cusSkypeMe = 'SKYPEME'


#{ Call failure reason
cfrUnknown = -1
cfrMiscError = 1
cfrUserDoesNotExist = 2
cfrUserIsOffline = 3
cfrNoProxyFound = 4
cfrSessionTerminated = 5
cfrNoCommonCodec = 6
cfrSoundIOError = 7
cfrRemoteDeviceError = 8
cfrBlockedByRecipient = 9
cfrRecipientNotFriend = 10
cfrNotAuthorizedByRecipient = 11
cfrSoundRecordingError = 12


#{ Call status
clsUnknown = 'NOT_AVAILABLE'
clsUnplaced = 'UNPLACED'
clsRouting = 'ROUTING'
clsEarlyMedia = 'EARLYMEDIA'
clsFailed = 'FAILED'
clsRinging = 'RINGING'
clsInProgress = 'INPROGRESS'
clsOnHold = 'ONHOLD'
clsFinished = 'FINISHED'
clsMissed = 'MISSED'
clsRefused = 'REFUSED'
clsBusy = 'BUSY'
clsCancelled = 'CANCELLED'
clsLocalHold = 'REDIAL_PENDING'
clsRemoteHold = 'REMOTEHOLD'
clsVoicemailBufferingGreeting = 'VM_BUFFERING_GREETING'
clsVoicemailPlayingGreeting = 'VM_PLAYING_GREETING'
clsVoicemailRecording = 'VM_RECORDING'
clsVoicemailUploading = 'VM_UPLOADING'
clsVoicemailSent = 'VM_SENT'
clsVoicemailCancelled = 'VM_CANCELLED'
clsVoicemailFailed = 'VM_FAILED'
clsTransferring = 'TRANSFERRING'
clsTransferred = 'TRANSFERRED'


#{ Call type
cltUnknown = 'UNKNOWN'
cltIncomingPSTN = 'INCOMING_PSTN'
cltOutgoingPSTN = 'OUTGOING_PSTN'
cltIncomingP2P = 'INCOMING_P2P'
cltOutgoingP2P = 'OUTGOING_P2P'


#{ Call history
chsAllCalls = 'ALL'
chsMissedCalls = 'MISSED'
chsIncomingCalls = 'INCOMING'
chsOutgoingCalls = 'OUTGOING'


#{ Call video status
cvsUnknown = 'UNKNOWN'
cvsNone = 'VIDEO_NONE'
cvsSendEnabled = 'VIDEO_SEND_ENABLED'
cvsReceiveEnabled = 'VIDEO_RECV_ENABLED'
cvsBothEnabled = 'VIDEO_BOTH_ENABLED'


#{ Call video send status
vssUnknown = 'UNKNOWN'
vssNotAvailable = 'NOT_AVAILABLE'
vssAvailable = 'AVAILABLE'
vssStarting = 'STARTING'
vssRejected = 'REJECTED'
vssRunning = 'RUNNING'
vssStopping = 'STOPPING'
vssPaused = 'PAUSED'


#{ Call IO device type
callIoDeviceTypeUnknown = 'UNKNOWN'
callIoDeviceTypeSoundcard = 'SOUNDCARD'
callIoDeviceTypePort = 'PORT'
callIoDeviceTypeFile = 'FILE'


#{ Chat message type
cmeUnknown = 'UNKNOWN'
cmeCreatedChatWith = 'CREATEDCHATWITH'
cmeSawMembers = 'SAWMEMBERS'
cmeAddedMembers = 'ADDEDMEMBERS'
cmeSetTopic = 'SETTOPIC'
cmeSaid = 'SAID'
cmeLeft = 'LEFT'
cmeEmoted = 'EMOTED'
cmePostedContacts = 'POSTEDCONTACTS'
cmeGapInChat = 'GAP_IN_CHAT'
cmeSetRole = 'SETROLE'
cmeKicked = 'KICKED'
cmeKickBanned = 'KICKBANNED'
cmeSetOptions = 'SETOPTIONS'
cmeSetPicture = 'SETPICTURE'
cmeSetGuidelines = 'SETGUIDELINES'
cmeJoinedAsApplicant = 'JOINEDASAPPLICANT'


#{ Chat message status
cmsUnknown = 'UNKNOWN'
cmsSending = 'SENDING'
cmsSent = 'SENT'
cmsReceived = 'RECEIVED'
cmsRead = 'READ'


#{ User sex
usexUnknown = 'UNKNOWN'
usexMale = 'MALE'
usexFemale = 'FEMALE'


#{ Buddy status
budUnknown = -1
budNeverBeenFriend = 0
budDeletedFriend = 1
budPendingAuthorization = 2
budFriend = 3


#{ Online status
olsUnknown = 'UNKNOWN'
olsOffline = 'OFFLINE'
olsOnline = 'ONLINE'
olsAway = 'AWAY'
olsNotAvailable = 'NA'
olsDoNotDisturb = 'DND'
olsInvisible = 'INVISIBLE'
olsSkypeOut = 'SKYPEOUT'
olsSkypeMe = 'SKYPEME'


#{ Chat leave reason
leaUnknown = ''
leaUserNotFound = 'USER_NOT_FOUND'
leaUserIncapable = 'USER_INCAPABLE'
leaAdderNotFriend = 'ADDER_MUST_BE_FRIEND'
leaAddedNotAuthorized = 'ADDED_MUST_BE_AUTHORIZED'
leaAddDeclined = 'ADD_DECLINED'
leaUnsubscribe = 'UNSUBSCRIBE'


#{ Chat status
chsUnknown = 'UNKNOWN'
chsLegacyDialog = 'LEGACY_DIALOG'
chsDialog = 'DIALOG'
chsMultiNeedAccept = 'MULTI_NEED_ACCEPT'
chsMultiSubscribed = 'MULTI_SUBSCRIBED'
chsUnsubscribed = 'UNSUBSCRIBED'


#{ Voicemail type
vmtUnknown = 'UNKNOWN'
vmtIncoming = 'INCOMING'
vmtDefaultGreeting = 'DEFAULT_GREETING'
vmtCustomGreeting = 'CUSTOM_GREETING'
vmtOutgoing = 'OUTGOING'


#{ Voicemail status
vmsUnknown = 'UNKNOWN'
vmsNotDownloaded = 'NOTDOWNLOADED'
vmsDownloading = 'DOWNLOADING'
vmsUnplayed = 'UNPLAYED'
vmsBuffering = 'BUFFERING'
vmsPlaying = 'PLAYING'
vmsPlayed = 'PLAYED'
vmsBlank = 'BLANK'
vmsRecording = 'RECORDING'
vmsRecorded = 'RECORDED'
vmsUploading = 'UPLOADING'
vmsUploaded = 'UPLOADED'
vmsDeleting = 'DELETING'
vmsFailed = 'FAILED'


#{ Voicemail failure reason
vmrUnknown = 'UNKNOWN'
vmrNoError = 'NOERROR'
vmrMiscError = 'MISC_ERROR'
vmrConnectError = 'CONNECT_ERROR'
vmrNoPrivilege = 'NO_VOICEMAIL_PRIVILEGE'
vmrNoVoicemail = 'NO_SUCH_VOICEMAIL'
vmrFileReadError = 'FILE_READ_ERROR'
vmrFileWriteError = 'FILE_WRITE_ERROR'
vmrRecordingError = 'RECORDING_ERROR'
vmrPlaybackError = 'PLAYBACK_ERROR'


#{ Group type
grpUnknown = 'UNKNOWN'
grpCustomGroup = 'CUSTOM_GROUP'
grpAllUsers = 'ALL_USERS'
grpAllFriends = 'ALL_FRIENDS'
grpSkypeFriends = 'SKYPE_FRIENDS'
grpSkypeOutFriends = 'SKYPEOUT_FRIENDS'
grpOnlineFriends = 'ONLINE_FRIENDS'
grpPendingAuthorizationFriends = 'UNKNOWN_OR_PENDINGAUTH_FRIENDS'
grpRecentlyContactedUsers = 'RECENTLY_CONTACTED_USERS'
grpUsersWaitingMyAuthorization = 'USERS_WAITING_MY_AUTHORIZATION'
grpUsersAuthorizedByMe = 'USERS_AUTHORIZED_BY_ME'
grpUsersBlockedByMe = 'USERS_BLOCKED_BY_ME'
grpUngroupedFriends = 'UNGROUPED_FRIENDS'
grpSharedGroup = 'SHARED_GROUP'
grpProposedSharedGroup = 'PROPOSED_SHARED_GROUP'


#{ Call channel type
cctUnknown = 'UNKNOWN'
cctDatagram = 'DATAGRAM'
cctReliable = 'RELIABLE'


#{ API security context
apiContextUnknown = 0
apiContextVoice = 1
apiContextMessaging = 2
apiContextAccount = 4
apiContextContacts = 8


#{ SMS message type
smsMessageTypeUnknown = 'UNKNOWN'
smsMessageTypeIncoming = 'INCOMING'
smsMessageTypeOutgoing = 'OUTGOING'
smsMessageTypeCCRequest = 'CONFIRMATION_CODE_REQUEST'
smsMessageTypeCCSubmit = 'CONFRIMATION_CODE_SUBMIT'


#{ SMS message status
smsMessageStatusUnknown = 'UNKNOWN'
smsMessageStatusReceived = 'RECEIVED'
smsMessageStatusRead = 'READ'
smsMessageStatusComposing = 'COMPOSING'
smsMessageStatusSendingToServer = 'SENDING_TO_SERVER'
smsMessageStatusSentToServer = 'SENT_TO_SERVER'
smsMessageStatusDelivered = 'DELIVERED'
smsMessageStatusSomeTargetsFailed = 'SOME_TARGETS_FAILED'
smsMessageStatusFailed = 'FAILED'


#{ SMS failure reason
smsFailureReasonUnknown = 'UNKNOWN'
smsFailureReasonMiscError = 'MISC_ERROR'
smsFailureReasonServerConnectFailed = 'SERVER_CONNECT_FAILED'
smsFailureReasonNoSmsCapability = 'NO_SMS_CAPABILITY'
smsFailureReasonInsufficientFunds = 'INSUFFICIENT_FUNDS'
smsFailureReasonInvalidConfirmationCode = 'INVALID_CONFIRMATION_CODE'
smsFailureReasonUserBlocked = 'USER_BLOCKED'
smsFailureReasonIPBlocked = 'IP_BLOCKED'
smsFailureReasonNodeBlocked = 'NODE_BLOCKED'
smsFailureReasonNoSenderIdCapability = 'NO_SENDERID_CAPABILITY'


#{ SMS target status
smsTargetStatusUnknown = 'UNKNOWN'
smsTargetStatusUndefined = 'TARGET_UNDEFINED'
smsTargetStatusAnalyzing = 'TARGET_ANALYZING'
smsTargetStatusAcceptable = 'TARGET_ACCEPTABLE'
smsTargetStatusNotRoutable = 'TARGET_NOT_ROUTABLE'
smsTargetStatusDeliveryPending = 'TARGET_DELIVERY_PENDING'
smsTargetStatusDeliverySuccessful = 'TARGET_DELIVERY_SUCCESSFUL'
smsTargetStatusDeliveryFailed = 'TARGET_DELIVERY_FAILED'


#{ Plug-in context
pluginContextUnknown = 'unknown'
pluginContextChat = 'chat'
pluginContextCall = 'call'
pluginContextContact = 'contact'
pluginContextMyself = 'myself'
pluginContextTools = 'tools'


#{ Plug-in contact type
pluginContactTypeUnknown = 'unknown'
pluginContactTypeAll = 'all'
pluginContactTypeSkype = 'skype'
pluginContactTypeSkypeOut = 'skypeout'


#{ File transfer type
fileTransferTypeIncoming = 'INCOMING'
fileTransferTypeOutgoing = 'OUTGOING'


#{ File transfer status
fileTransferStatusNew = 'NEW'
fileTransferStatusConnecting = 'CONNECTING'
fileTransferStatusWaitingForAccept = 'WAITING_FOR_ACCEPT'
fileTransferStatusTransferring = 'TRANSFERRING'
fileTransferStatusTransferringOverRelay = 'TRANSFERRING_OVER_RELAY'
fileTransferStatusPaused = 'PAUSED'
fileTransferStatusRemotelyPaused = 'REMOTELY_PAUSED'
fileTransferStatusCancelled = 'CANCELLED'
fileTransferStatusCompleted = 'COMPLETED'
fileTransferStatusFailed = 'FAILED'


#{ File transfer failure reason
fileTransferFailureReasonSenderNotAuthorized = 'SENDER_NOT_AUTHORIZED'
fileTransferFailureReasonRemotelyCancelled = 'REMOTELY_CANCELLED'
fileTransferFailureReasonFailedRead = 'FAILED_READ'
fileTransferFailureReasonFailedRemoteRead = 'FAILED_REMOTE_READ'
fileTransferFailureReasonFailedWrite = 'FAILED_WRITE'
fileTransferFailureReasonFailedRemoteWrite = 'FAILED_REMOTE_WRITE'
fileTransferFailureReasonRemoteDoesNotSupportFT = 'REMOTE_DOES_NOT_SUPPORT_FT'
fileTransferFailureReasonRemoteOfflineTooLong = 'REMOTE_OFFLINE_TOO_LONG'


#{ Chat member role
chatMemberRoleUnknown = 'UNKNOWN'
chatMemberRoleCreator = 'CREATOR'
chatMemberRoleMaster = 'MASTER'
chatMemberRoleHelper = 'HELPER'
chatMemberRoleUser = 'USER'
chatMemberRoleListener = 'LISTENER'
chatMemberRoleApplicant = 'APPLICANT'


#{ My chat status
chatStatusUnknown = 'UNKNOWN'
chatStatusConnecting = 'CONNECTING'
chatStatusWaitingRemoteAccept = 'WAITING_REMOTE_ACCEPT'
chatStatusAcceptRequired = 'ACCEPT_REQUIRED'
chatStatusPasswordRequired = 'PASSWORD_REQUIRED'
chatStatusSubscribed = 'SUBSCRIBED'
chatStatusUnsubscribed = 'UNSUBSCRIBED'
chatStatusDisbanded = 'CHAT_DISBANDED'
chatStatusQueuedBecauseChatIsFull = 'QUEUED_BECAUSE_CHAT_IS_FULL'
chatStatusApplicationDenied = 'APPLICATION_DENIED'
chatStatusKicked = 'KICKED'
chatStatusBanned = 'BANNED'
chatStatusRetryConnecting = 'RETRY_CONNECTING'


#{ Chat options
chatOptionJoiningEnabled = 1
chatOptionJoinersBecomeApplicants = 2
chatOptionJoinersBecomeListeners = 4
chatOptionHistoryDisclosed = 8
chatOptionUsersAreListeners = 16
chatOptionTopicAndPictureLockedForUsers = 32


#{ Chat type
chatTypeUnknown = 'UNKNOWN'
chatTypeDialog = 'DIALOG'
chatTypeLegacyDialog = 'LEGACY_DIALOG'
chatTypeLegacyUnsubscribed = 'LEGACY_UNSUBSCRIBED'
chatTypeMultiChat = 'MULTICHAT'
chatTypeSharedGroup = 'SHAREDGROUP'

#{ Window state
wndUnknown = 'UNKNOWN'
wndNormal = 'NORMAL'
wndMinimized = 'MINIMIZED'
wndMaximized = 'MAXIMIZED'
wndHidden = 'HIDDEN'
