#![cfg(not(feature = "no-entrypoint"))]

use std::ops::Deref;

use solana_program::declare_id;
use borsh::{BorshDeserialize, BorshSerialize};
use solana_program::account_info::next_account_info;
use solana_program::program::invoke;

use solana_program::{
    account_info::AccountInfo,
    entrypoint,
    entrypoint::ProgramResult,
    instruction::{AccountMeta, Instruction},
    pubkey::Pubkey,
};
use std::rc::Rc;


declare_id!("My11111111111111111111111111111111111111112");

#[derive(BorshDeserialize, BorshSerialize)]
pub enum Arcade {
    play,
}


entrypoint!(process_instruction);
    fn process_instruction(
        program_id: &Pubkey,
        accounts: &[AccountInfo],
        instruction_data: &[u8],
    ) -> ProgramResult {
        let account_iter = &mut accounts.iter();
        let program = next_account_info(account_iter)?;
        let data_account = next_account_info(account_iter)?;
        let user = next_account_info(account_iter)?;
        let user_data = next_account_info(account_iter)?;
        let my_pg = next_account_info(account_iter)?;
        let sp = next_account_info(account_iter)?;

        // for debug
        {
            // let str = Rc::deref(&Rc::clone(&data_account.data)).borrow().deref();
            // msg!(&format!("{:?}", Rc::deref(&Rc::clone(&data_account.data)).borrow().deref()));
        }
        let forgotten:[u8; 8]  = Rc::deref(&Rc::clone(&data_account.data)).borrow().deref()[24..32].try_into().unwrap();
        let atBottom:[u8; 8] = Rc::deref(&Rc::clone(&data_account.data)).borrow().deref()[36..44].try_into().unwrap();
        let somewhere:[u8; 32] = Rc::deref(&Rc::clone(&data_account.data)).borrow().deref()[44..76].try_into().unwrap();
        let stuckInGap:[u8; 8] = Rc::deref(&Rc::clone(&data_account.data)).borrow().deref()[96..104].try_into().unwrap(); 
        let lookForIt:[u8; 8] = Rc::deref(&Rc::clone(&data_account.data)).borrow().deref()[120..128].try_into().unwrap();

        {
            let mut cont: Vec<u8> = vec![85, 43, 21, 196, 243, 127, 55, 65];

            cont.append(&mut somewhere.to_vec());
    
            let find_bytes32 = Instruction::new_with_bytes(
                program.key.clone(),
                &cont,
                vec![
                    AccountMeta::new(data_account.key.clone(), false),
                    AccountMeta::new(user.key.clone(), true),
                    AccountMeta::new_readonly(program.key.clone(), false),
                ],
            );
    
            invoke(&find_bytes32, 
                &[
                    user_data.clone(),
                    data_account.clone(),
                    user.clone(),
                    program.clone(),
                    my_pg.clone(),
                    sp.clone(),
            ]);
        }

        {
            let mut cont: Vec<u8> = vec![52, 228, 208, 77, 202, 97, 52, 46];
            let mut cont2: Vec<u8> = vec![8,0,0,0];
            
            cont.append(&mut cont2);
            cont.append(&mut lookForIt.to_vec());
    
            let find_string = Instruction::new_with_bytes(
                program.key.clone(),
                &cont,
                vec![
                    AccountMeta::new(data_account.key.clone(), false),
                    AccountMeta::new(user.key.clone(), true),
                    AccountMeta::new_readonly(program.key.clone(), false),
                ],
            );
    
            invoke(&find_string, 
                &[
                    user_data.clone(),
                    data_account.clone(),
                    user.clone(),
                    program.clone(),
                    my_pg.clone(),
                    sp.clone(),
            ]);
        }

        {
            let mut cont: Vec<u8> = vec![9, 229, 75, 5, 193, 115, 105, 171];
            let mut s1 = BorshSerialize::try_to_vec("Token Dispenser").unwrap();
    
            cont.append(&mut s1);
            cont.append(&mut forgotten.to_vec());
    
            let find_string_uint64 = Instruction::new_with_bytes(
                program.key.clone(),
                &cont,
                vec![
                    AccountMeta::new(data_account.key.clone(), false),
                    AccountMeta::new(user.key.clone(), true),
                    AccountMeta::new_readonly(program.key.clone(), false),
                ],
            );
    
            invoke(&find_string_uint64, 
                &[
                    user_data.clone(),
                    data_account.clone(),
                    user.clone(),
                    program.clone(),
                    my_pg.clone(),
                    sp.clone(),
            ]);
        }

        {
            let mut cont: Vec<u8> = vec![9, 229, 75, 5, 193, 115, 105, 171];
            let mut s1 = BorshSerialize::try_to_vec("Token Counter").unwrap();
    
            cont.append(&mut s1);
            cont.append(&mut stuckInGap.to_vec());
    
            let find_string_uint64 = Instruction::new_with_bytes(
                program.key.clone(),
                &cont,
                vec![
                    AccountMeta::new(data_account.key.clone(), false),
                    AccountMeta::new(user.key.clone(), true),
                    AccountMeta::new_readonly(program.key.clone(), false),
                ],
            );
    
            invoke(&find_string_uint64, 
                &[
                    user_data.clone(),
                    data_account.clone(),
                    user.clone(),
                    program.clone(),
                    my_pg.clone(),
                    sp.clone(),
            ]);
        }

        {
            let mut cont: Vec<u8> = vec![9, 229, 75, 5, 193, 115, 105, 171];
            let mut s1 = BorshSerialize::try_to_vec("Arcade Machine").unwrap();
    
            cont.append(&mut s1);
            cont.append(&mut atBottom.to_vec());
    
            let find_string_uint64 = Instruction::new_with_bytes(
                program.key.clone(),
                &cont,
                vec![
                    AccountMeta::new(data_account.key.clone(), false),
                    AccountMeta::new(user.key.clone(), true),
                    AccountMeta::new_readonly(program.key.clone(), false),
                ],
            );
    
            invoke(&find_string_uint64, 
                &[
                    user_data.clone(),
                    data_account.clone(),
                    user.clone(),
                    program.clone(),
                    my_pg.clone(),
                    sp.clone(),
            ]);
        }

        {
            let mut cont: Vec<u8> = vec![213, 157, 193, 142, 228, 56, 248, 150];
    
            let play = Instruction::new_with_bytes(
                program.key.clone(),
                &cont,
                vec![
                    AccountMeta::new(data_account.key.clone(), false),
                    AccountMeta::new(user.key.clone(), true),
                    AccountMeta::new_readonly(program.key.clone(), false),
                ],
            );
    
            invoke(&play, 
                &[
                    user_data.clone(),
                    data_account.clone(),
                    user.clone(),
                    program.clone(),
                    my_pg.clone(),
                    sp.clone(),
            ]);
        }
       
        Ok(())        
    }